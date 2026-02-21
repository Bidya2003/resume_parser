<p><small>Best View in <a href="https://github.com/settings/appearance">Light Mode</a> and Desktop Site (Recommended)</small></p><br/>

![AI-Resume-Analyzer](https://github.com/Bidya2003/resume_parser/blob/main/screenshots/demo.png)

<div align="center">
  <h1> AI RESUME Evaluation System </h1>
  <p>A Tool for Resume Analysis, Predictions and Recommendations</p>
  <!-- Badges -->
  <p>
    <img src="https://badges.frapsoft.com/os/v2/open-source.svg?v=103" alt="open source" />
    <img src="https://img.shields.io/github/languages/top/deepakpadhi986/AI-Resume-Analyzer?color=red" alt="language" />
    <img src="https://img.shields.io/github/languages/code-size/deepakpadhi986/AI-Resume-Analyzer?color=informational" alt="code size" />
    </a>
  </p>
  
  <!--links-->
  <h4>
    <a href="#preview-https://resumeparser-e52qkc7qgewyqir6jpfb5u.streamlit.app/">View Demo</a>
    <span> · </span>
    <a href="#setup--installation-">Installation</a>
    <span> · </span>
    <a href="mailto:dnoobnerd@gmail.com?subject=I%20Want%20The%20Project%20Report%20of%20AI-RESUME-ANALYZER%20(2022%20 %2023)&body=Here%20Are%20My%20Details%20%F0%9F%98%89%0D%0A%0D%0AOrganization%2FCollege%20Name%3A%20%0D%0A%0D%0AFull%20Name%3A%20%0D%0A%0D%0AGitHub%20Profile%20%3A%20%0D%0A%0D%0AFrom%20where%20did%20you%20get%20to%20know%20about%20this%20project%3A%0D%0A%0D%0APurpose%20of%20asking%20project%20report%20(describe)%3A%0D%0A%0D%0A%0D%0AIf%20the%20above%20information%20satisfy%20your%20identity%20you%20will%20get%20the%20report%20to%20your%20email.">Project Report</a>
  </h4>
  <p>
    <small align="justify">
      Built with 🤍 by 
      <a href="">Bidyajani Maji</a>
     </small>
  </p>
</div><br/><br/>

## About the Project 🥱
<div align="center">
    <br/><img src="https://github.com/Bidya2003/resume_parser/blob/main/screenshots/Hailuo_Image__The%20Brain%20Behind%20AI%20Resume%20Ev_436178469640138757.png" alt="screenshot" /><br/><br/>
    <p align="justify"> 
      A tool which parses information from a resume using natural language processing and finds the keywords, cluster them onto sectors based on their keywords. 
      And lastly show recommendations, predictions, analytics to the applicant / recruiter based on keyword matching.
    </p>
</div>

## Scope 😲
i. It can be used for getting all the resume data into a structured tabular format and csv as well, so that the organization can use those data for analytics purposes

ii. By providing recommendations, predictions and overall score user can improve their resume and can keep on testing it on our tool

iii. And it can increase more traffic to our tool because of user section

iv. It can be used by colleges to get insight of students and their resume before placements

v. Also, to get analytics for roles which users are mostly looking for

vi. To improve this tool by getting feedbacks

<!-- TechStack -->
## Tech Stack 🍻
<details>
  <summary>Frontend</summary>
  <ul>
    <li><a href="https://streamlit.io/">Streamlit</a></li>
    <li><a href="https://developer.mozilla.org/en-US/docs/Learn/HTML">HTML</a></li>
    <li><a href="https://developer.mozilla.org/en-US/docs/Web/CSS">CSS</a></li>
    <li><a href="https://developer.mozilla.org/en-US/docs/Learn/JavaScript">JavaScript</a></li>
  </ul>
</details>

<details>
  <summary>Backend</summary>
  <ul>
    <li><a href="https://streamlit.io/">Streamlit</a></li>
    <li><a href="https://www.python.org/">Python</a></li>
  </ul>
</details>

<details>
<summary>Database</summary>
  <ul>
    <li><a href="https://www.mysql.com/">MySQL</a></li>
  </ul>
</details>

<details>
<summary>Modules</summary>
  <ul>
    <li><a href="https://pandas.pydata.org/">pandas</a></li>
    <li><a href="https://github.com/OmkarPathak/pyresparser">pyresparser</a></li>
    <li><a href="https://pypi.org/project/pdfminer3/">pdfminer3</a></li>
    <li><a href="https://plotly.com/">Plotly</a></li>
    <li><a href="https://www.nltk.org/">NLTK</a></li>
  </ul>
</details>

<!-- Features -->
## Features 🤦‍♂️
### Client: -
- Fetching Location and Miscellaneous Data

  Using Parsing Techniques to fetch
- Basic Info
- Skills
- Keywords

Using logical programs, it will recommend

- Skills that can be added
- Resume Summary
- Predicted job role
- Course wise skill match Analysis
- Course and certificates
- Resume tips and ideas
- Overall Score
- Interview & Resume tip videos

### Admin: -
- Get all applicant’s data into tabular format
- Download user’s data into csv file
- View all saved uploaded pdf in Uploaded Resume folder
- Get user feedback and ratings
  
  Pie Charts for: -
- Ratings
- Predicted field / roles
- Experience level
- Resume score
- User count
- City
- State
- Country

### Feedback: -
- Form filling
- Rating from 1 – 5
- Show overall ratings pie chart
- Past user comments history 

## Requirements 😅
### Have these things installed to make your process smooth 
1) Python (3.9.12) https://www.python.org/downloads/release/python-3912/
2) MySQL https://www.mysql.com/downloads/
3) Visual Studio Code **(Prefered Code Editor)** https://code.visualstudio.com/Download

## Setup & Installation 👀

To run this project, perform the following tasks 😨

Download the code file manually or via git
```bash
git clone https://github.com/Bidya2003/resume_parser.git
```

Create a virtual environment and activate it **(recommended)**

Open your command prompt and change your project directory to ```AI-Resume-Analyzer``` and run the following command 
```bash
python -m venv venvapp

cd venvapp/Scripts

activate

```

Downloading packages from ```requirements.txt``` inside ``App`` folder
```bash
cd../..

cd App

pip install -r requirements.txt

python -m spacy download en_core_web_sm

```

After installation is finished create a Database ```cv```

And change user credentials inside ```App.py```

Go to ```venvapp\Lib\site-packages\pyresparser``` folder

And replace the ```resume_parser.py``` with ```resume_parser.py``` 

which was provided by me inside ```pyresparser``` folder

``Congratulations 🥳😱 your set-up 👆 and installation is finished 😵🤯``

I hope that your ``venvapp`` is activated and working directory is inside ``App``

Run the ```App.py``` file using
```bash
streamlit run App.py

```

## Known Error 🤪
If ``GeocoderUnavailable`` error comes up then just check your internet connection and network speed

## Usage
- After the setup it will do stuff's automatically
- You just need to upload a resume and see it's magic
- Try first with my resume uploaded in ``Uploaded_Resumes`` folder
- Admin userid is ``admin`` and password is ``admin@resume-analyzer``

<!-- Roadmap -->
## Roadmap 🛵
* [x] Predict user experience level.
* [x] Add resume scoring criteria for skills and projects.
* [x] Added fields and recommendations for web, android, ios, data science.
* [ ] Add more fields for other roles, and its recommendations respectively. 
* [x] Fetch more details from users resume.
* [ ] View individual user details.

## Preview

### Client Side

**Main Screen**

![Screenshot](https://github.com/Bidya2003/resume_parser/blob/main/screenshots/AI%20Resume%20Evaluation%20System%20and%203%20more%20pages%20-%20Profile%201%20-%20Microsoft%E2%80%8B%20Edge%2019-10-2025%2008_10_22.png)

**Resume Upload**

![Screenshot](https://github.com/Bidya2003/resume_parser/blob/main/screenshots/AI%20Resume%20Evaluation%20System%20and%203%20more%20pages%20-%20Profile%201%20-%20Microsoft%E2%80%8B%20Edge%2019-10-2025%2008_18_00.png)

**Resume Summary Generator**

![Screenshot](https://github.com/Bidya2003/resume_parser/blob/main/screenshots/AI%20Resume%20Evaluation%20System%20and%203%20more%20pages%20-%20Profile%201%20-%20Microsoft%E2%80%8B%20Edge%2019-10-2025%2008_20_07.png)

**Personal Informations & Current Skills**

![Screenshot](https://github.com/Bidya2003/resume_parser/blob/main/screenshots/AI%20Resume%20Evaluation%20System%20and%203%20more%20pages%20-%20Profile%201%20-%20Microsoft%E2%80%8B%20Edge%2019-10-2025%2008_20_39.png)

**Course & Skills Recommendation**

![Screenshot](https://github.com/Bidya2003/resume_parser/blob/main/screenshots/AI%20Resume%20Evaluation%20System%20and%203%20more%20pages%20-%20Profile%201%20-%20Microsoft%E2%80%8B%20Edge%2019-10-2025%2008_21_36.png)

**Course wise Skill match analysis**

![Screenshot](https://github.com/Bidya2003/resume_parser/blob/main/screenshots/AI%20Resume%20Evaluation%20System%20and%203%20more%20pages%20-%20Profile%201%20-%20Microsoft%E2%80%8B%20Edge%2019-10-2025%2008_22_10.png)

**Tips and Overall Score**

![Screenshot](https://github.com/Bidya2003/resume_parser/blob/main/screenshots/AI%20Resume%20Evaluation%20System%20and%203%20more%20pages%20-%20Profile%201%20-%20Microsoft%E2%80%8B%20Edge%2019-10-2025%2008_22_35.png)

**Video Recommendation**

![Screenshot](https://github.com/Bidya2003/resume_parser/blob/main/screenshots/AI%20Resume%20Evaluation%20System%20and%203%20more%20pages%20-%20Profile%201%20-%20Microsoft%E2%80%8B%20Edge%2019-10-2025%2008_22_44.png)

### Feedback

**Feedback Form**

![Screenshot](https://github.com/Bidya2003/resume_parser/blob/main/screenshots/AI%20Resume%20Evaluation%20System%20and%204%20more%20pages%20-%20Profile%201%20-%20Microsoft%E2%80%8B%20Edge%2019-10-2025%2009_28_53.png)

**Overall Rating Analysis and Comment History**

![Screenshot](https://github.com/Bidya2003/resume_parser/blob/main/screenshots/AI%20Resume%20Evaluation%20System%20and%204%20more%20pages%20-%20Profile%201%20-%20Microsoft%E2%80%8B%20Edge%2019-10-2025%2009_29_02.png)

### Admin

**Login**

![Screenshot](https://github.com/Bidya2003/resume_parser/blob/main/screenshots/AI%20Resume%20Evaluation%20System%20and%203%20more%20pages%20-%20Profile%201%20-%20Microsoft%E2%80%8B%20Edge%2019-10-2025%2008_22_59.png)

**User Count and it's data**

![Screenshot](https://github.com/Bidya2003/resume_parser/blob/main/screenshots/AI%20Resume%20Evaluation%20System%20and%203%20more%20pages%20-%20Profile%201%20-%20Microsoft%E2%80%8B%20Edge%2019-10-2025%2008_23_53.png)

**Exported csv file**

![Screenshot](https://github.com/Bidya2003/resume_parser/blob/main/screenshots/AI%20Resume%20Evaluation%20System%20and%204%20more%20pages%20-%20Profile%201%20-%20Microsoft%E2%80%8B%20Edge%2019-10-2025%2009_35_17.png)

**Pie Chart Analytical Representation of clusters**

![Screenshot](https://github.com/Bidya2003/resume_parser/blob/main/screenshots/AI%20Resume%20Evaluation%20System%20and%203%20more%20pages%20-%20Profile%201%20-%20Microsoft%E2%80%8B%20Edge%2019-10-2025%2008_24_14.png)

![Screenshot](https://github.com/Bidya2003/resume_parser/blob/main/screenshots/AI%20Resume%20Evaluation%20System%20and%203%20more%20pages%20-%20Profile%201%20-%20Microsoft%E2%80%8B%20Edge%2019-10-2025%2008_24_24.png)

![Screenshot](https://github.com/Bidya2003/resume_parser/blob/main/screenshots/AI%20Resume%20Evaluation%20System%20and%204%20more%20pages%20-%20Profile%201%20-%20Microsoft%E2%80%8B%20Edge%2019-10-2025%2009_47_30.png)

![Screenshot](https://github.com/Bidya2003/resume_parser/blob/main/screenshots/AI%20Resume%20Evaluation%20System%20and%204%20more%20pages%20-%20Profile%201%20-%20Microsoft%E2%80%8B%20Edge%2019-10-2025%2009_47_40.png)

![Screenshot](https://github.com/Bidya2003/resume_parser/blob/main/screenshots/AI%20Resume%20Evaluation%20System%20and%204%20more%20pages%20-%20Profile%201%20-%20Microsoft%E2%80%8B%20Edge%2019-10-2025%2009_48_00.png)

![Screenshot](https://github.com/Bidya2003/resume_parser/blob/main/screenshots/AI%20Resume%20Evaluation%20System%20and%204%20more%20pages%20-%20Profile%201%20-%20Microsoft%E2%80%8B%20Edge%2019-10-2025%2009_48_28.png)

![Screenshot](https://github.com/Bidya2003/resume_parser/blob/main/screenshots/AI%20Resume%20Evaluation%20System%20and%204%20more%20pages%20-%20Profile%201%20-%20Microsoft%E2%80%8B%20Edge%2019-10-2025%2009_48_36.png)

### Built with 🤍 AI RESUME Evaluation Syatem by <a href="">Bidyajani Maji</a>
