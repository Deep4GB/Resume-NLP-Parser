import streamlit as st
import sqlite3
from resume_parser import extract_resume_info_from_pdf, extract_contact_number_from_resume, extract_education_from_resume, \
    extract_experience, suggest_skills_for_job, show_colored_skills, calculate_resume_score, extract_resume_info

# Function to create a table for PDFs in SQLite database if it doesn't exist
def create_table():
    conn = sqlite3.connect('data/user_pdfs.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_uploaded_pdfs (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            data BLOB NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert PDF into the SQLite database
def insert_pdf(name, data):
    conn = sqlite3.connect('data/user_pdfs.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO user_uploaded_pdfs (name, data) VALUES (?, ?)', (name, data))
    conn.commit()
    conn.close()

def process_user_mode():
    create_table()  # Create table if it doesn't exist

    st.title("Resume Parser using NLP")
    uploaded_file = st.file_uploader("Upload a PDF resume", type="pdf")

    if uploaded_file:
        st.write("File uploaded successfully!")

        pdf_name = uploaded_file.name
        pdf_data = uploaded_file.getvalue()

        # Insert the uploaded PDF into the database
        insert_pdf(pdf_name, pdf_data)

        pdf_text = extract_resume_info_from_pdf(uploaded_file)
        resume_info = extract_resume_info(pdf_text)

        st.markdown('<hr>', unsafe_allow_html=True)
        st.header("Extracted Information:")
        st.write(f"First Name: {resume_info['first_name']}")
        st.write(f"Last Name: {resume_info['last_name']}")
        st.write(f"Email: {resume_info['email']}")

        # Fix the function call for extracting the phone number
        contact_number = extract_contact_number_from_resume(pdf_text)
        st.write(f"Phone Number:  +{contact_number}")
        
        st.write(f"Degree/Major: {resume_info['degree_major']}")

        st.markdown('<hr>', unsafe_allow_html=True)
        st.header("Education:")
        education_info = extract_education_from_resume(pdf_text)
        st.write(', '.join(education_info) if education_info else "No education information found")

        st.markdown('<hr>', unsafe_allow_html=True)
        st.header("Skills:")
        show_colored_skills(resume_info['skills'])

        st.markdown('<hr>', unsafe_allow_html=True)
        st.header("Experience:")
        experience_info = extract_experience(pdf_text)
        st.write(f"Level of Experience: {experience_info['level_of_experience']}")
        st.write(f"Suggested Position: {experience_info['suggested_position']}")

        st.markdown('<hr>', unsafe_allow_html=True)
        st.header("Resume Score:")
        resume_score = calculate_resume_score(resume_info)
        st.write(f"**Resume Score:** {resume_score}/100")

        # Displaying a custom-styled progress bar with gradient colors
        percentage = resume_score
        percentage_str = str(percentage)
        bar = (
            f'<div style="background: linear-gradient(90deg, #f63366 {percentage_str}%, #d6d6d6 {percentage_str}%);'
            'height: 30px; border-radius: 5px; display: flex; align-items: center;">'
            f'<div style="color: white; text-align: center; width: 100%;">{percentage}%</div>'
            '</div>'
        )
        st.markdown(bar, unsafe_allow_html=True)

        st.markdown('<hr>', unsafe_allow_html=True)
        st.header("Suggested Skills for the Desired Job:")
        desired_job = st.text_input("Enter the job you are looking for:")
        suggested_skills = suggest_skills_for_job(desired_job)
        st.write(suggested_skills)

if __name__ == '__main__':
    process_user_mode()
