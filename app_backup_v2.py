import streamlit as st
from PyPDF2 import PdfReader
import re
import pandas as pd

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

with st.sidebar:
    st.title("Resume Analyzer")
    st.info("""
    Features:
    ✅ Resume Parsing
    ✅ ATS Score
    ✅ Role Prediction
    ✅ Skill Gap Analysis
    ✅ JD Matching
    ✅ Resume Suggestions
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

    st.write("🛠 Skills")

    for skill in found_skills:
        st.write("✅", skill)

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

    st.subheader("Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Resume Score", f"{score}/100")

    with col2:
        st.metric("ATS Score", f"{ats_score}/100")

    with col3:
        st.metric("JD Match", f"{match_score}%")

    chart_data = pd.DataFrame(
        {
            "Score": [
                score,
                ats_score,
                match_score
            ]
        },
        index=[
            "Resume",
            "ATS",
            "JD Match"
        ]
    )

    st.bar_chart(chart_data)

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

        st.write(
            f"Match Score: {match_score}%"
        )

        st.write("Matched Skills:")

        for skill in matched_skills:
            st.write("✅", skill)

    suggestions = get_suggestions(
        score,
        ats_score,
        missing_skills
    )

    st.subheader(
        "Resume Improvement Suggestions"
    )

    for suggestion in suggestions:
        st.warning(suggestion)