import streamlit as st
from PyPDF2 import PdfReader
import re

from modules.resume_scorer import calculate_score
from modules.role_predictor import predict_role
from modules.ats_checker import calculate_ats_score
from modules.skill_gap import find_missing_skills

st.title("📄 Smart Resume Analyzer")

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

if uploaded_file:

    st.success("Resume uploaded successfully!")

    pdf = PdfReader(uploaded_file)

    text = ""

    for page in pdf.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted

    # Display Resume Content
    st.subheader("Resume Content")

    st.text_area(
        "Resume Text",
        text,
        height=300
    )

    # Extract Email
    email = re.findall(
        r'[\w\.-]+@[\w\.-]+',
        text
    )

    # Extract Phone
    phone = re.findall(
        r'\+?\d[\d\s-]{8,}',
        text
    )

    # Extract Skills
    skills_list = [
        "Python",
        "Java",
        "C++",
        "SQL",
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Flask",
        "Django",
        "MongoDB",
        "Git",
        "TypeScript",
        "Pandas",
        "NumPy",
        "Excel"
    ]

    found_skills = []

    for skill in skills_list:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    # Extracted Information
    st.subheader("Extracted Information")

    if email:
        st.write("📧 Email:", email[0])

    if phone:
        st.write("📱 Phone:", phone[0])

    st.write("🛠 Skills:")

    for skill in found_skills:
        st.write("✅", skill)

    # Resume Score
    score = calculate_score(text)

    st.subheader("Resume Score")

    st.progress(score / 100)

    st.write(f"Score: {score}/100")

    # Role Prediction
    role = predict_role(found_skills)

    st.subheader("Recommended Role")

    st.success(role)

    # ATS Score
    ats_score = calculate_ats_score(text)

    st.subheader("ATS Compatibility Score")

    st.progress(ats_score / 100)

    st.write(f"ATS Score: {ats_score}/100")

    # Skill Gap Analysis
    missing_skills = find_missing_skills(
        role,
        found_skills
    )

    st.subheader("Skill Gap Analysis")

    if missing_skills:

        for skill in missing_skills:
            st.write("❌", skill)

    else:
        st.success(
            "No major skill gaps found!"
        )