import streamlit as st
import spacy
import nltk
import os
import csv
import fitz  # PyMuPDF library for PDF parsing
import base64
import random

nltk.download('punkt')

# Load the spaCy model for English
nlp = spacy.load('en_core_web_sm')

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
    skills_keywords = load_keywords('data/skills.csv')
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
    return {'first_name': first_name, 'last_name': last_name, 'email': email, 'degree_major': degree_major, 'skills': skills}

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

def main():
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

if __name__ == "__main__":
    main()
