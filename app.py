import streamlit as st
import spacy
import nltk
import os
import csv
import fitz  # PyMuPDF library for PDF parsing
import base64
import random
import pandas as pd

# Additional libraries
nltk.download('punkt')

# Load the spaCy model for English
nlp = spacy.load('en_core_web_sm')

# Feedback DataFrame
feedback_data = pd.DataFrame(columns=['User Name', 'Feedback', 'Timestamp'])

def load_keywords(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        return set(row[0] for row in reader)

def extract_name(first_lines):
    first_lines_doc = nlp(first_lines)
    for ent in first_lines_doc.ents:
        if ent.label_ == 'PERSON':
            names = ent.text.split()
            if len(names) >= 2 and names[0].istitle() and names[1].istitle():
                return names[0], ' '.join(names[1:])
    return "", ""

def extract_email(resume_text):
    matcher = spacy.matcher.Matcher(nlp.vocab)
    email_pattern = [{'LIKE_EMAIL': True}]
    matcher.add('EMAIL', [email_pattern])

    doc = nlp(resume_text)
    matches = matcher(doc)
    for match_id, start, end in matches:
        if match_id == nlp.vocab.strings['EMAIL']:
            return doc[start:end].text
    return ""

def extract_skills(resume_text):
    skills_keywords = load_keywords('data/newSkills.csv')
    skills = set()
    for keyword in skills_keywords:
        if keyword.lower() in resume_text.lower():
            skills.add(keyword)
    return skills

def extract_major(resume_text):
    major_keywords = load_keywords('data/majors.csv')
    for keyword in major_keywords:
        if keyword.lower() in resume_text.lower():
            return keyword
    return ""

def extract_experience(resume_text):
    nlp = spacy.load('en_core_web_sm')

    # Process the resume text using spaCy
    doc = nlp(resume_text)

    # Extract verbs (action words) from the resume
    verbs = [token.text for token in doc if token.pos_ == 'VERB']

    # Analyze the extracted verbs to determine the level of experience
    if any(keyword in verbs for keyword in ['lead', 'manage', 'direct']):
        level_of_experience = "Senior"
    elif any(keyword in verbs for keyword in ['develop', 'design', 'analyze']):
        level_of_experience = "Mid-Senior"
    elif any(keyword in verbs for keyword in ['assist', 'support', 'collaborate']):
        level_of_experience = "Mid-Junior"
    else:
        level_of_experience = "Entry Level"

    # Suggest a position based on the observed verbs
    suggested_position = suggest_position(verbs)

    return {
        'level_of_experience': level_of_experience,
        'suggested_position': suggested_position
    }

def load_positions_keywords(file_path):
    positions_keywords = {}
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            position = row['position']
            keywords = [keyword.lower() for keyword in row['keywords'].split(',')]
            positions_keywords[position] = keywords
    return positions_keywords


def suggest_position(verbs):
    positions_keywords = load_positions_keywords('data/position.csv')
    verbs = [verb.lower() for verb in verbs]
    for position, keywords in positions_keywords.items():
        if any(keyword in verbs for keyword in keywords):
            return position

    return "Position Not Identified"

def extract_resume_info_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text += page.get_text()
    return text

def show_colored_skills(skills):
    st.write(', '.join(skills))

def calculate_resume_score(resume_info):
    # Your scoring logic here
    # For example, you can assign scores based on the presence of specific information
    score = 0
    if resume_info['first_name'] and resume_info['last_name']:
        score += 25
    if resume_info['email']:
        score += 25
    if resume_info['degree_major']:
        score += 25
    if resume_info['skills']:
        score += 25
    return score

def extract_resume_info(text):
    first_lines = '\n'.join(text.splitlines()[:10])
    first_name, last_name = extract_name(first_lines)
    email = extract_email(text)
    skills = extract_skills(text)
    degree_major = extract_major(text)
    experience = extract_experience(text)

    return {'first_name': first_name, 'last_name': last_name, 'email': email, 'degree_major': degree_major, 'skills': skills, 'experience': experience}

def suggest_skills_for_job(desired_job):
    job_skills_mapping = {
        'software engineer': ['Python', 'Java', 'JavaScript', 'React', 'Django', 'Git'],
        'data scientist': ['Python', 'R', 'Machine Learning', 'Statistics', 'SQL'],
        'graphic designer': ['Adobe Photoshop', 'Illustrator', 'UI/UX Design', 'Typography'],
        # Add more job-skill mappings as needed
    }

    desired_job_lower = desired_job.lower()
    if desired_job_lower in job_skills_mapping:
        suggested_skills = job_skills_mapping[desired_job_lower]
        return suggested_skills
    else:
        return []

def show_pdf(uploaded_file):
    try:
        with open(uploaded_file.name, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    except AttributeError:
        base64_pdf = base64.b64encode(uploaded_file.read()).decode('utf-8')

    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def authenticate_admin(username, password):
    # Hardcoded username and password for demonstration purposes
    hardcoded_username = "deep"
    hardcoded_password = "dp10"

    return username == hardcoded_username and password == hardcoded_password


def main():
    st.set_page_config(page_title="Resume Parser", page_icon="✅")

    # Sidebar
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox("Choose an option", ["Users", "Recruiters", "Admin", "Feedback"])


    if app_mode == "Users":
        st.title("Resume Parser using NLP")
        uploaded_file = st.file_uploader("Upload a PDF resume", type="pdf")
        if uploaded_file:
            st.write("File uploaded successfully!")

            # Extract text from the uploaded PDF
            pdf_text = extract_resume_info_from_pdf(uploaded_file)

            # Extract information from the text
            resume_info = extract_resume_info(pdf_text)

            # Display the extracted information
            st.header("Extracted Information:")
            st.write(f"First Name: {resume_info['first_name']}")
            st.write(f"Last Name: {resume_info['last_name']}")
            st.write(f"Email: {resume_info['email']}")
            st.write(f"Degree/Major: {resume_info['degree_major']}")
            st.header("Skills:")
            show_colored_skills(resume_info['skills'])
            st.header("Experience:")
            # Extract and display experience information
            experience_info = extract_experience(pdf_text)
            st.write(f"Level of Experience: {experience_info['level_of_experience']}")
            st.write(f"Suggested Position: {experience_info['suggested_position']}")


            # Calculate and display the resume score
            resume_score = calculate_resume_score(resume_info)
            st.header("Resume Score:")
            st.progress(resume_score)

            st.header("Suggested Skills for the Desired Job:")
            # Get user input for the desired job
            desired_job = st.text_input("Enter the job you are looking for:")

            # Suggest skills based on the desired job
            suggested_skills = suggest_skills_for_job(desired_job)
            st.write(suggested_skills)


    elif app_mode == "Recruiters":
        st.title("Recruiter's Panel")
        st.warning("Still under development!!")


    elif app_mode == "Admin":
        st.title("Admin Panel")
        st.subheader("Authentication Required")

        # Admin authentication
        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")
        if st.button("Login"):
            if authenticate_admin('deep', 'dp10'):
                st.success("Authentication successful!")

                # Admin functionalities go here

                # Display feedback data
                st.subheader("Feedback Data")
                st.write(feedback_data)
            else:
                st.error("Authentication failed. Please try again.")


    elif app_mode == "Feedback":
        st.title("Feedback Section")
        st.subheader("Provide Feedback")

        # Feedback Form
        user_name = st.text_input("Your Name:")
        feedback = st.text_area("Provide feedback on the resume parser:", height=100)
        if st.button("Submit Feedback"):
            feedback_data.loc[len(feedback_data)] = [user_name, feedback, pd.to_datetime("now")]
            st.success("Feedback submitted successfully!")


if __name__ == "__main__":
    main()
