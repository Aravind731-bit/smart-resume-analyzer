import streamlit as st
from PyPDF2 import PdfReader
import re
import pandas as pd
from fpdf import FPDF

from modules.resume_scorer import calculate_score
from modules.role_predictor import predict_role
from modules.ats_checker import calculate_ats_score
from modules.skill_gap import find_missing_skills
from modules.jd_matcher import calculate_match
from modules.suggestions import get_suggestions

st.set_page_config(
    page_title="Smart Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Smart Resume Analyzer")
st.caption("AI-Powered Resume Analysis & ATS Optimization Tool")

st.sidebar.title("📄 Resume Analyzer")

st.sidebar.success("Version 2.0")

st.sidebar.markdown("""
### Features

✅ Resume Parsing

✅ ATS Analysis

✅ Role Prediction

✅ Skill Gap Detection

✅ JD Matching

✅ Resume Suggestions

✅ Report Download
""")

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

if uploaded_file:

    st.success("Resume uploaded successfully!")

    pdf = PdfReader(uploaded_file)

    text = ""

    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    st.subheader("Resume Content")
    st.text_area("Resume Text", text, height=300)

    email = re.findall(r'[\w\.-]+@[\w\.-]+', text)
    phone = re.findall(r'\+?\d[\d\s-]{8,}', text)

    skills_list = [
        "Python", "Java", "C++", "SQL",
        "HTML", "CSS", "JavaScript",
        "React", "Flask", "Django",
        "MongoDB", "Git", "TypeScript",
        "Pandas", "NumPy", "Excel"
    ]

    found_skills = []  

    for skill in skills_list:
        if skill.lower() in text.lower():
            found_skills.append(skill)
    st.subheader("Extracted Information")

    if email:
        st.write("📧 Email:", email[0])

    if phone:
        st.write("📱 Phone:", phone[0])

    linkedin = re.findall(  
        r'https?://(?:www\.)?linkedin\.com/[^\s]+',
        text
    )

    github = re.findall(
        r'https?://(?:www\.)?github\.com/[^\s]+',
        text
    )

    if linkedin:
        st.write("🔗 LinkedIn:", linkedin[0])

    if github:
        st.write("💻 GitHub:", github[0])

    st.write("🛠 Skills")

    for skill in found_skills:
        st.write("✅", skill)

    st.subheader("📈 Resume Statistics") 

    st.subheader("🛠 Skills Distribution")

    skill_df = pd.DataFrame({
        "Skill": found_skills,
        "Count": [1] * len(found_skills)
    })

    st.bar_chart(skill_df.set_index("Skill"))
 
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Skills Found", len(found_skills))

    with col2:
        st.metric("Resume Words", len(text.split()))

    with col3:
        st.metric("Pages", len(pdf.pages))
    
    score = calculate_score(text)
    ats_score = calculate_ats_score(text)
    role = predict_role(found_skills)

    missing_skills = find_missing_skills(
        role,
        found_skills
    )

    jd_text = st.text_area(
        "Paste Job Description Here"
    )

    match_score = 0
    matched_skills = []

    if jd_text:
        
        match_score, matched_skills = calculate_match(
            found_skills,
            jd_text
        )

    st.subheader("📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Resume Score", f"{score}/100")

    with col2:
        st.metric("ATS Score", f"{ats_score}/100")

    with col3:
        st.metric("JD Match", f"{match_score}%")
    if match_score >= 80:
        st.success("🎯 Excellent Job Match")
    elif match_score >= 60:
        st.warning("👍 Good Job Match")
    elif match_score > 0:
        st.error("⚠️ Low Job Match")

    chart_data = pd.DataFrame({
        "Category": ["Resume", "ATS", "JD Match"],
        "Score": [score, ats_score, match_score]
    })

    st.bar_chart(chart_data.set_index("Category"))
   
    st.subheader("📈 Resume Score Meter")

    st.progress(score / 100)

    st.write(f"Overall Resume Score: {score}/100")

    st.subheader("🤖 ATS Compatibility")

    st.progress(ats_score / 100)

    st.write(f"ATS Score: {ats_score}/100")

    if score >= 80:
        st.success("🟢 Strong Resume")
    elif score >= 60:
        st.warning("🟡 Average Resume")
    else:
        st.error("🔴 Needs Improvement")

    st.subheader("Recommended Role")
    st.success(role)

    st.subheader("Skill Gap Analysis")

    if missing_skills:
        for skill in missing_skills:
            st.write("❌", skill)
    else:
        st.success("No major skill gaps found!")

    if jd_text:
        st.subheader("Job Description Matching")

        st.progress(match_score / 100)

        st.write(f"Match Score: {match_score}%")

    if match_score >= 80:
         st.write("Your resume is highly aligned with this job description.")
    elif match_score >= 60:
        st.write("Your resume matches many requirements, but can be improved.")
    else:
        st.write("Consider adding more relevant skills from the job description.")

        st.write("Matched Skills:")

    for skill in matched_skills:
        st.write("✅", skill)

    suggestions = get_suggestions(
        score,
        ats_score,
        missing_skills
    )

    st.subheader("Resume Improvement Suggestions")

    for suggestion in suggestions:
        st.warning(suggestion)

    st.subheader("📥 Download Analysis Report")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Resume Analysis Report", ln=True)

    pdf.cell(200, 10, txt=f"Resume Score: {score}/100", ln=True)
    pdf.cell(200, 10, txt=f"ATS Score: {ats_score}/100", ln=True)
    pdf.cell(200, 10, txt=f"Recommended Role: {role}", ln=True)

    pdf.cell(200, 10, txt="Detected Skills:", ln=True)

    for skill in found_skills:
        pdf.cell(200, 10, txt=skill, ln=True)

    pdf.cell(200, 10, txt="Missing Skills:", ln=True)

    for skill in missing_skills:
        pdf.cell(200, 10, txt=skill, ln=True)

    pdf.output("report.pdf")

    with open("report.pdf", "rb") as file:
        st.download_button(
            "📄 Download Report",
            file,
            file_name="Resume_Report.pdf"
        )

st.markdown("---")

st.subheader("📌 Project Summary")

st.info("""
Smart Resume Analyzer is an AI-powered application that:
• Extracts resume information
• Calculates ATS compatibility
• Predicts suitable job roles
• Detects skill gaps
• Matches resumes with job descriptions
• Generates improvement suggestions
""")

st.caption("Developed by Aravind Goud")