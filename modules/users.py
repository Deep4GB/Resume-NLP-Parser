
# users.py
import streamlit as st
from resume_parser import extract_resume_info_from_pdf, extract_resume_info, calculate_resume_score, show_colored_skills, extract_experience, suggest_skills_for_job

def process_user_mode():
    st.title("Resume Parser using NLP")
    uploaded_file = st.file_uploader("Upload a PDF resume", type="pdf")

    if uploaded_file:
        st.write("File uploaded successfully!")

        pdf_text = extract_resume_info_from_pdf(uploaded_file)
        resume_info = extract_resume_info(pdf_text)

        st.header("Extracted Information:")
        st.write(f"First Name: {resume_info['first_name']}")
        st.write(f"Last Name: {resume_info['last_name']}")
        st.write(f"Email: {resume_info['email']}")
        st.write(f"Degree/Major: {resume_info['degree_major']}")

        st.header("Skills:")
        show_colored_skills(resume_info['skills'])

        st.header("Experience:")
        experience_info = extract_experience(pdf_text)
        st.write(f"Level of Experience: {experience_info['level_of_experience']}")
        st.write(f"Suggested Position: {experience_info['suggested_position']}")

        resume_score = calculate_resume_score(resume_info)
        st.header("Resume Score:")
        st.progress(resume_score)

        st.header("Suggested Skills for the Desired Job:")
        desired_job = st.text_input("Enter the job you are looking for:")
        suggested_skills = suggest_skills_for_job(desired_job)
        st.write(suggested_skills)
