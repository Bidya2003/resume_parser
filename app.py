
import os
import streamlit as st
import pandas as pd
import base64
import time
import datetime
import random
import io
import re
import nltk
nltk.download('stopwords')
nltk.download('punkt')

from PIL import Image
from pyresparser import ResumeParser
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage
from streamlit_tags import st_tags
import pymysql
import nltk
import yt_dlp as ydl
import plotly.express as px
from fuzzywuzzy import fuzz
from transformers import pipeline
from dotenv import load_dotenv
import os


from courses import (
    ds_course, sd_course, fullstack_course, frontend_course, backend_course,
    ai_course, ml_course, web_course, android_course, ios_course, uiux_course,
    resume_videos, interview_videos
)

# Ensure upload folder exists
os.makedirs('./Uploaded_Resumes', exist_ok=True)

# Download stopwords (for pyresparser)
nltk.download('stopwords')

# Streamlit Page Config
st.set_page_config(
    page_title="AI Resume Evaluation System",
    layout="wide",
    page_icon="🟢"
)

# === Dark Glassmorphic CSS with Emerald-Teal Accent ===
st.markdown(
    """
    <style>
    /* App background */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(1200px 600px at 10% 10%, rgba(6, 95, 70, 0.18), transparent 8%),
                    radial-gradient(1000px 500px at 90% 90%, rgba(14, 116, 144, 0.12), transparent 10%),
                    linear-gradient(180deg, #071724 0%, #08121A 100%);
        color: #E6FFFA;
        font-family: "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }

    /* Sidebar glass */
    [data-testid="stSidebar"] {
        background: rgba(7,12,15,0.65);
        backdrop-filter: blur(8px) saturate(120%);
        border-right: 1px solid rgba(255,255,255,0.03);
    }

    /* Title */
    .title-centered {
        text-align: center;
        font-size: 48px;
        font-weight: 800;
        margin-bottom: 6px;
        background: linear-gradient(90deg, #34D399, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .small-muted {
        text-align:center;
        color:#9CA3AF;
        font-size:14px;
        margin-bottom: 12px;
    }

    /* Glass card */
    .card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.04);
        padding: 14px 18px;
        border-radius: 12px;
        box-shadow: 0 8px 30px rgba(3,7,10,0.55);
        backdrop-filter: blur(8px);
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }
    .card:hover { transform: translateY(-4px); box-shadow: 0 14px 40px rgba(2,6,8,0.6); }

    /* Badges */
    .badge-green { background: rgba(52,211,153,0.12); color: #34D399; padding:6px 12px; border-radius:8px; font-weight:600; }
    .badge-red   { background: rgba(239,68,68,0.08); color: #FCA5A5; padding:6px 12px; border-radius:8px; font-weight:600; }

    /* Buttons */
    div.stButton > button {
        width: 100%;
        height: 46px;
        border-radius: 10px;
        background: linear-gradient(90deg, #2dd4bf, #06b6d4);
        color: #041014;
        font-weight: 700;
        border: none;
        box-shadow: 0 8px 20px rgba(6,182,178,0.12);
        transition: transform 0.14s ease, box-shadow 0.14s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 18px 40px rgba(6,182,178,0.18);
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        border-radius: 10px;
        border: 1px dashed rgba(255,255,255,0.04);
        background: rgba(255,255,255,0.02);
        padding: 10px;
    }

    /* Divider */
    hr, .stDivider { border: none; height: 2px; background: linear-gradient(90deg, rgba(52,211,153,0.12), rgba(6,182,178,0.12)); margin: 28px 0; }

    /* Small muted text inside cards */
    .small-muted-inside { font-size:13px; color:#9CA3AF; }

    /* Make iframes responsive */
    iframe { border-radius: 10px; }

    /* Streamlit tags spacing fix */
    .stTags { margin-top: 8px; margin-bottom: 12px; }
    </style>
    """,
    unsafe_allow_html=True
)

# Helper Functions

def fetch_yt_video(link):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,  # Only fetch metadata
    }
    with ydl.YoutubeDL(ydl_opts) as ydl_instance:
        info_dict = ydl_instance.extract_info(link, download=False)
        return info_dict.get('title', 'Unknown Title')

def get_table_download_link(df, filename, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}" style="color:#34D399;">{text}</a>'
    return href

def pdf_reader(file_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(file_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)

    text = fake_file_handle.getvalue()
    converter.close()
    fake_file_handle.close()
    return text

def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def course_recommender(course_list):
    st.subheader("Courses & Certificates Recommendations 🎓")
    rec_course = []
    no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 6)
    random.shuffle(course_list)
    for c_idx, (c_name, c_link) in enumerate(course_list):
        st.markdown(f"({c_idx+1}) [{c_name}]({c_link})")
        rec_course.append(c_name)
        if c_idx + 1 == no_of_reco:
            break
    return rec_course

# Lazy load summarizer to avoid slow startup
summarizer = None

def load_summarizer():
    global summarizer
    if summarizer is None:
        with st.spinner("Loading summarization model..."):
            summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def generate_resume_summary(resume_text):
    load_summarizer()
    clean_text = " ".join(resume_text.split()[:2000])
    summary = summarizer(clean_text, max_length=120, min_length=40, do_sample=False)
    return summary[0]['summary_text']

# Database Connection
load_dotenv()

try:
    connection = pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        db=os.getenv('DB_NAME')
    )
    cursor = connection.cursor()
    print("✅ Database connected successfully")
# except Exception as e:
#     st.error(f"Database connection failed: {e}")
#     st.stop()

except Exception as e:
    st.warning("⚠ Database not available. Running in Cloud Mode (No DB).")
    connection = None
    cursor = None


def insert_data(name, email, res_score, timestamp, no_of_pages, reco_field, cand_level, skills, recommended_skills, courses):
    if not cursor:
        st.warning("Feedback storage disabled (No DB Mode)")
        return
    DB_table_name = 'user_data'
    insert_sql = f"INSERT INTO {DB_table_name} VALUES (0, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    rec_values = (name, email, str(res_score), timestamp, str(no_of_pages), reco_field, cand_level, skills, recommended_skills, courses)
    if cursor:
        cursor.execute(insert_sql, rec_values)
        connection.commit()

# Streamlit Page Config (kept to original)
st.set_page_config(
    page_title="AI Resume Evaluation System",
    layout="wide"
)

def run():
    # Top title area centered
    colL, colC, colR = st.columns([1, 2, 1])
    with colC:
        st.markdown('<div class="title-centered">AI Resume Evaluation System</div>', unsafe_allow_html=True)
        st.markdown('<div class="small-muted">Upload your resume to get summary, skills & course recommendations</div>', unsafe_allow_html=True)
        st.write("")

    st.sidebar.markdown("# Choose User")
    activities = ["User", "Admin", "Feedback"]
    choice = st.sidebar.selectbox("Choose among the given options:", activities)
    link = '[©Developed by Bidyajani Maji](https://www.linkedin.com/in/bidyajani-maji)'
    st.sidebar.markdown(link, unsafe_allow_html=True)

    # Ensure DB and table exist (kept same as before)
    if cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS CV;")
        table_sql = """
            CREATE TABLE IF NOT EXISTS user_data (
                ID INT NOT NULL AUTO_INCREMENT,
                Name varchar(500) NOT NULL,
                Email_ID VARCHAR(500) NOT NULL,
                resume_score VARCHAR(8) NOT NULL,
                Timestamp VARCHAR(50) NOT NULL,
                Page_no VARCHAR(5) NOT NULL,
                Predicted_Field BLOB NOT NULL,
                User_level BLOB NOT NULL,
                Actual_skills BLOB NOT NULL,
                Recommended_skills BLOB NOT NULL,
                Recommended_courses BLOB NOT NULL,
                PRIMARY KEY (ID)
            );
        """
        cursor.execute(table_sql)

    if choice == "User":
        st.markdown('<div class="card"><strong>Upload your resume, and get smart recommendations</strong></div>', unsafe_allow_html=True)
        pdf_file = st.file_uploader("Choose your Resume (PDF)", type=["pdf"])
        if pdf_file is not None:
            with st.spinner('Uploading your Resume...'):
                time.sleep(0.5)
            save_path = os.path.join('Uploaded_Resumes', pdf_file.name)
            try:
                with open(save_path, "wb") as f:
                    f.write(pdf_file.getbuffer())
            except Exception as e:
                st.error(f"Error saving file: {e}")
                return

            with st.expander("Preview uploaded resume (click to open)"):
                try:
                    show_pdf(save_path)
                except Exception as e:
                    st.error(f"Cannot preview PDF: {e}")

            # Try parsing
            try:
                resume_data = ResumeParser(save_path).get_extracted_data()
            except Exception as e:
                st.error(f"Error parsing resume: {e}")
                resume_data = None

            if resume_data:
                resume_text = ""
                try:
                    resume_text = pdf_reader(save_path)
                except Exception as e:
                    st.error(f"Error reading PDF text: {e}")
                    resume_text = ""

                st.markdown("---")
                st.subheader("🧠 AI Resume Summary Generator")

                # Maintain summary persistently in session_state
                if "resume_summary" not in st.session_state:
                    st.session_state.resume_summary = ""

                # Two-column layout for summary controls + display
                sum_left, sum_right = st.columns([2, 3])

                with sum_left:
                    if st.button("Generate Resume Summary"):
                        if resume_text:
                            with st.spinner("Analyzing and generating summary..."):
                                summary = generate_resume_summary(resume_text)
                                st.session_state.resume_summary = summary  # persist
                            st.success("✅ Resume Summary Generated Successfully!")
                        else:
                            st.error("Could not read resume text for summarization.")

                    if st.button("Clear Summary"):
                        st.session_state.resume_summary = ""

                with sum_right:
                    if st.session_state.resume_summary:
                        st.markdown('<div class="card"><h4 style="margin-bottom:6px">📋 Generated Summary</h4></div>', unsafe_allow_html=True)
                        st.markdown(f"<div class='card'><div class='small-muted-inside'>{st.session_state.resume_summary}</div></div>", unsafe_allow_html=True)

                # Add some spacing
                st.markdown("<br><br>", unsafe_allow_html=True)
                st.markdown("---")

                # Basic info card
                left, right = st.columns([2, 3])
                with left:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    try:
                        st.markdown(f"**Name:** {resume_data.get('name','-')}")
                        st.markdown(f"**Email:** {resume_data.get('email','-')}")
                        st.markdown(f"**Contact:** {resume_data.get('mobile_number','-')}")
                        st.markdown(f"**Pages:** {resume_data.get('no_of_pages', 0)}")
                    except Exception as e:
                        st.write(f"Error showing basic info: {e}")
                    st.markdown('</div>', unsafe_allow_html=True)

                with right:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    cand_level = ''
                    pages = resume_data.get('no_of_pages', 0)
                    if pages == 1:
                        cand_level = "Fresher"
                        st.markdown('<div class="badge-red">You are at Fresher level</div>', unsafe_allow_html=True)
                    elif pages == 2:
                        cand_level = "Intermediate"
                        st.markdown('<div class="badge-green">You are at Intermediate level</div>', unsafe_allow_html=True)
                    elif pages >= 3:
                        cand_level = "Experienced"
                        st.markdown('<div class="badge-green">You are at Experienced level</div>', unsafe_allow_html=True)
                    st.write("")
                    st.markdown('<div class="small-muted-inside">Tip: Use the course check buttons below to see matched vs missing skills per course.</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                # Show skills
                st.write("")
                st_tags(label='Your Current Skills', text='Detected from resume', value=resume_data.get('skills', []), key='1')

                # Build your keyword lists (same as before)
                ds_keyword = ['data science','python','statistic','pandas','numpy','matplotlib','seaborn','sql','machine learning','tensorflow','pytorch','nlp','spark','hadoop','flask','api']
                sd_keyword = ['software development','python','java','c++','git','oop', 'aws','api','gcp','azure','data structure']
                fullStack_keyword = ['fullstack','html', 'css', 'javascript', 'git' , 'node.js' ,'python' ,'react.js' ,'angular' ,'vue.js' ,'express.js' ,'django','flask','sql','mongodb','api','crud','redux','contextapi','jwt','auth','docker','kubernetes','aws','azure','gcp']
                frontend_keyword = ['frontend','html','css', 'javascript','flexbox','grid','react','vue','angular','sass','less','git','es6+','async','promises','redux','api','jest','cypress']
                backend_keyword = ['backend','python','node.js','java','http','rest','sql','django','flask','express.js','springboot','api','orm','sql alchemy','mongoose','authentication','redis','memcached','microservices','cloud','ci','cd','pipeline']
                web_keyword = ['web','react', 'django', 'node js', 'php', 'laravel', 'magento', 'wordpress', 'javascript', 'angular js', 'c#', 'flask']
                android_keyword = ['android','flutter','kotlin','xml','kivy','java','layouts','recycleview','fragments','room','retrofit','volley','mvvm','jetpack','animations','playstore deploy']
                ios_keyword = ['ios','swift','cocoa','xcode','uikit','swiftui','storyboards','coredata','networking','animations','deploy','framework']
                uiux_keyword = ['ux','figma','adobe xd','balsamiq','ui','wireframes','photoshop','illustrator']
                ai_keyword = ['artificial intelligence','python','numpy','pandas','matplotlib','machine learning', 'models','scikit-learn','cnn','rnn','transformers','nlp','reinforcement','gpu acceleration']
                ml_keyword = ['machine learning','python','statistic','linear regression','logistic regression','decision tree','random forest','svm','knn','pca','neural network','deep learning','tensorflow','pytorch','tuning','deploy']

                resume_full_text = resume_text.lower()

                def fuzzy_match(keyword, text, threshold=80):
                    if keyword.lower() in text:
                        return True
                    target = keyword.lower().split()
                    tokens = text.split()
                    n = len(target)
                    if n == 0:
                        return False
                    for i in range(len(tokens) - n + 1):
                        window = " ".join(tokens[i:i+n])
                        if fuzz.ratio(keyword.lower(), window) >= threshold:
                            return True
                    for t in tokens:
                        if fuzz.ratio(keyword.lower(), t) >= threshold:
                            return True
                    return False

                course_keywords = {
                    'Data Science': ds_keyword,
                    'Web Development': web_keyword,
                    'Software Development': sd_keyword,
                    'Full-Stack Development': fullStack_keyword,
                    'Frontend Development': frontend_keyword,
                    'Backend Development': backend_keyword,
                    'Android Development': android_keyword,
                    'IOS Development': ios_keyword,
                    'Artificial Intelligence': ai_keyword,
                    'Machine Learning': ml_keyword,
                    'UI-UX Development': uiux_keyword
                }

                course_match_count = {}
                for course, keywords in course_keywords.items():
                    count = sum(1 for keyword in keywords if fuzzy_match(keyword, resume_full_text))
                    course_match_count[course] = count

                reco_field = max(course_match_count, key=course_match_count.get)
                recommended_skills = course_keywords[reco_field]

                st.success(f"Our analysis says you are looking for **{reco_field}** jobs.")

                recourse_dict = {
                    'Data Science': ds_course,
                    'Web Development': web_course,
                    'Software Development': sd_course,
                    'Full-Stack Development': fullstack_course,
                    'Frontend Development': frontend_course,
                    'Backend Development': backend_course,
                    'Android Development': android_course,
                    'IOS Development': ios_course,
                    'Artificial Intelligence': ai_course,
                    'Machine Learning': ml_course,
                    'UI-UX Development': uiux_course
                }
                rec_course = recourse_dict.get(reco_field, [])
                rec_course = course_recommender(rec_course)

                missing_skills = [skill for skill in recommended_skills if not fuzzy_match(skill, resume_full_text)]

                st_tags(
                    label='### Recommended skills for you (missing in your resume)',
                    text='Only skills that are not detected in your resume are shown here',
                    value=missing_skills,
                    key='2'
                )

                st.markdown("---")
                st.subheader("🔍 Explore Course-wise Skill Match Analysis")
                course_names = list(course_keywords.keys())
                cols = st.columns(3)
                for idx, course in enumerate(course_names):
                    col = cols[idx % 3]
                    with col:
                        if st.button(course, key=f"button_{course}"):
                            matched = [kw for kw in course_keywords[course] if fuzzy_match(kw, resume_full_text)]
                            missing = [kw for kw in course_keywords[course] if not fuzzy_match(kw, resume_full_text)]
                            mcol, ncol = st.columns([1,1])
                            with mcol:
                                st.markdown(f"<div class='card'><h4 style='margin-bottom:6px'>✅ Matched ({len(matched)})</h4>", unsafe_allow_html=True)
                                if matched:
                                    with st.expander("Show matched skills"):
                                        st.write(", ".join(matched))
                                else:
                                    st.write("None found")
                                st.markdown("</div>", unsafe_allow_html=True)
                            with ncol:
                                st.markdown(f"<div class='card'><h4 style='margin-bottom:6px'>❌ Missing ({len(missing)})</h4>", unsafe_allow_html=True)
                                if missing:
                                    with st.expander("Show missing skills"):
                                        st.write(", ".join(missing))
                                else:
                                    st.write("None — great!")
                                st.markdown("</div>", unsafe_allow_html=True)
                            st.info("You can work on the missing skills to improve your fit for this field.")
                            if missing:
                                st.markdown(f"**Suggested next steps:** consider improving skills: {', '.join(missing[:5])} ...")
                            else:
                                st.markdown("**Nice!** Your resume already covers core keywords for this course.")

                st.markdown("---")
                st.subheader("Resume Tips & Ideas 💡")
                resume_score = 0
                lower_text = resume_text.lower()
                if 'objective' in lower_text:
                    resume_score += 20
                    st.markdown('<div class="badge-green">[+] You have added Objective</div>', unsafe_allow_html=True)
                if 'experience' in lower_text:
                    resume_score += 20
                    st.markdown('<div class="badge-green">[+] You have Experience section</div>', unsafe_allow_html=True)
                if 'hobbies' in lower_text or 'interests' in lower_text:
                    resume_score += 20
                    st.markdown('<div class="badge-green">[+] You have Hobbies/Interests</div>', unsafe_allow_html=True)
                if 'achievements' in lower_text:
                    resume_score += 20
                    st.markdown('<div class="badge-green">[+] You have Achievements</div>', unsafe_allow_html=True)
                if 'project' in lower_text or 'projects' in lower_text:
                    resume_score += 20
                    st.markdown('<div class="badge-green">[+] You have Projects</div>', unsafe_allow_html=True)

                st.subheader("Resume Score")
                my_bar = st.progress(0)
                for percent_complete in range(resume_score):
                    time.sleep(0.01)
                    my_bar.progress(percent_complete + 1)
                st.success(f'**Your Resume Writing Score: {resume_score}**')
                st.warning("Note: This score is a simple heuristic based on presence of sections.")

                ts = time.time()
                cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                timestamp = f'{cur_date}_{cur_time}'

                insert_data(
                    resume_data.get('name',''),
                    resume_data.get('email',''),
                    resume_score,
                    timestamp,
                    resume_data.get('no_of_pages', 0),
                    reco_field,
                    cand_level,
                    str(resume_data.get('skills', [])),
                    str(recommended_skills),
                    str(rec_course)
                )

                st.markdown("---")
                st.header("Bonus: Resume & Interview Videos")
                video_col1, video_col2 = st.columns(2)
                with video_col1:
                    st.subheader("Resume Writing Tips")
                    resume_vid = random.choice(resume_videos)
                    st.markdown(f"**{fetch_yt_video(resume_vid)}**")
                    st.video(resume_vid)
                with video_col2:
                    st.subheader("Interview Tips")
                    interview_vid = random.choice(interview_videos)
                    st.markdown(f"**{fetch_yt_video(interview_vid)}**")
                    st.video(interview_vid)

            else:
                st.error('Something went wrong while parsing your resume.')
        else:
            st.info("🔼 Please upload a PDF resume to begin.")
            
    # FEEDBACK SECTION
            
            
    elif choice == 'Feedback':   

        # ---------------------------
        # 🕒 Timestamp Generation
        # ---------------------------
        ts = time.time()
        cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        timestamp = str(cur_date + '_' + cur_time)

        st.title("💬 Feedback Section")
        st.write("We value your opinion! Please share your experience with our Resume Analyzer.")

        # ---------------------------
        # ⚙️ Function to Insert Feedback into DB
        # ---------------------------
        def insertf_data(feed_name, feed_email, feed_score, comments, timestamp):
            try:
                DB_table_name = 'user_feedback'
                cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {DB_table_name} (
                        feed_id INT NOT NULL AUTO_INCREMENT,
                        feed_name VARCHAR(100),
                        feed_email VARCHAR(100),
                        feed_score INT,
                        comments TEXT,
                        timestamp VARCHAR(50),
                        PRIMARY KEY(feed_id)
                    )
                """)
                insert_sql = f"""
                    INSERT INTO {DB_table_name} 
                    (feed_name, feed_email, feed_score, comments, timestamp)
                    VALUES (%s, %s, %s, %s, %s)
                """
                rec_values = (feed_name, feed_email, feed_score, comments, timestamp)
                cursor.execute(insert_sql, rec_values)
                connection.commit()
            except Exception as e:
                st.error(f"❌ Error inserting feedback data: {e}")

        # ---------------------------
        # 🧾 Feedback Form
        # ---------------------------
        with st.form("my_form"):
            st.write("### Please fill out this form")
            feed_name = st.text_input('👤 Name')
            feed_email = st.text_input('📧 Email')
            feed_score = st.slider('⭐ Rate Us From 1 - 5', 1, 5)
            comments = st.text_area('💭 Comments')
            submitted = st.form_submit_button("Submit ✅")

            if submitted:
                if feed_name and feed_email:
                    insertf_data(feed_name, feed_email, feed_score, comments, timestamp)
                    st.success("🎉 Thanks! Your feedback was recorded successfully.")
                    st.balloons()
                else:
                    st.warning("⚠️ Please enter your name and email before submitting.")

        # ---------------------------
        # 📊 Show Feedback Analytics
        # ---------------------------
        try:
            query = 'SELECT * FROM user_feedback'
            plotfeed_data = pd.read_sql(query, connection)

            # Rating Pie Chart
            labels = plotfeed_data.feed_score.unique()
            values = plotfeed_data.feed_score.value_counts()

            st.subheader("📈 Past User Ratings")
            fig = px.pie(
                values=values,
                names=labels,
                title="Distribution of User Ratings (1 - 5)",
                color_discrete_sequence=px.colors.sequential.Aggrnyl
            )
            st.plotly_chart(fig)

            # User Comments Table
            cursor.execute('SELECT feed_name, comments FROM user_feedback')
            plfeed_cmt_data = cursor.fetchall()

            st.subheader("💬 User Comments")
            dff = pd.DataFrame(plfeed_cmt_data, columns=['User', 'Comment'])
            st.dataframe(dff, width=1000)

        except Exception as e:
            st.info("No feedback data available yet. Be the first to give feedback! 😊")

    

    
    else:  # Admin Side
        st.success('Welcome to Admin Side')
        ad_user = st.text_input("Username")
        ad_password = st.text_input("Password", type='password')

        if st.button('Login'):
            if ad_user == 'briit' and ad_password == 'briit123':
                st.success("Welcome Dr Briit !")

                if not cursor:
                    st.error("Admin panel unavailable in Cloud Mode (No Database)")
                    return

                cursor.execute("SELECT * FROM user_data")

                data = cursor.fetchall()
                df = pd.DataFrame(data, columns=[
                    'ID', 'Name', 'Email', 'Resume Score', 'Timestamp',
                    'Total Page', 'Predicted_Field', 'User_level',
                    'Actual_skills', 'Recommended_skills', 'Recommended_course'
                ])

                # Decode byte columns if necessary
                for col in ['Predicted_Field', 'User_level', 'Actual_skills', 'Recommended_skills', 'Recommended_course']:
                    df[col] = df[col].apply(lambda x: x.decode() if isinstance(x, (bytes, bytearray)) else str(x))

                # ✅ Add dummy data for missing columns (for visualization)
                if 'IP_add' not in df.columns:
                    df['IP_add'] = [f"192.168.0.{i+1}" for i in range(len(df))]
                if 'City' not in df.columns:
                    city_list = ['Kolkata', 'Delhi', 'Mumbai', 'Chennai', 'Bangalore'] * ((len(df) // 5) + 1)
                    df['City'] = city_list[:len(df)]

                if 'State' not in df.columns:
                    state_list = ['West Bengal', 'Delhi', 'Maharashtra', 'Tamil Nadu', 'Karnataka'] * ((len(df) // 5) + 1)
                    df['State'] = state_list[:len(df)]
                if 'Country' not in df.columns:
                    df['Country'] = ['India'] * len(df)

                # 🧾 Show Table
                st.header("User's Data")
                st.dataframe(df)
                st.markdown(get_table_download_link(df, 'User_Data.csv', 'Download Report'), unsafe_allow_html=True)

                # 📊 Pie chart 1: Predicted Field
                labels = df['Predicted_Field'].unique()
                values = df['Predicted_Field'].value_counts()
                st.subheader("Pie-Chart for Predicted Field Recommendation")
                fig = px.pie(df, values=values, names=labels, title='Predicted Field according to the Skills')
                st.plotly_chart(fig)

                # 📊 Pie chart 2: User Level
                labels_level = df['User_level'].unique()
                values_level = df['User_level'].value_counts()
                st.subheader("Pie-Chart for User's Experienced Level")
                fig2 = px.pie(df, values=values_level, names=labels_level, title="User's Experienced Level")
                st.plotly_chart(fig2)

                # 📊 Pie chart 3: Resume Score
                labels = df['Resume Score'].unique()
                values = df['Resume Score'].value_counts()
                st.subheader("**Pie-Chart for Resume Score**")
                fig3 = px.pie(df, values=values, names=labels, title='From 1 to 100 💯', color_discrete_sequence=px.colors.sequential.Agsunset)
                st.plotly_chart(fig3)

                # 📊 Pie chart 4: Users (IP-based)
                labels = df['IP_add'].unique()
                values = df['IP_add'].value_counts()
                st.subheader("**Pie-Chart for Users App Used Count**")
                fig4 = px.pie(df, values=values, names=labels, title='Usage Based On IP Address 👥', color_discrete_sequence=px.colors.sequential.Magma)
                st.plotly_chart(fig4)

                # 📊 Pie chart 5: City
                labels = df['City'].unique()
                values = df['City'].value_counts()
                st.subheader("**Pie-Chart for City**")
                fig5 = px.pie(df, values=values, names=labels, title='Usage Based On City 🌆', color_discrete_sequence=px.colors.sequential.Jet)
                st.plotly_chart(fig5)

                # 📊 Pie chart 6: State
                labels = df['State'].unique()
                values = df['State'].value_counts()
                st.subheader("**Pie-Chart for State**")
                fig6 = px.pie(df, values=values, names=labels, title='Usage Based on State 🚉', color_discrete_sequence=px.colors.sequential.PuBu_r)
                st.plotly_chart(fig6)

                # 📊 Pie chart 7: Country
                labels = df['Country'].unique()
                values = df['Country'].value_counts()
                st.subheader("**Pie-Chart for Country**")
                fig7 = px.pie(df, values=values, names=labels, title='Usage Based on Country 🌏', color_discrete_sequence=px.colors.sequential.Purpor_r)
                st.plotly_chart(fig7)


            else:
                st.error("Wrong ID & Password Provided")

if __name__ == "__main__":
    run()
