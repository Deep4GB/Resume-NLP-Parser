import streamlit as st
import spacy
from spacy.matcher import Matcher
import csv
import fitz  # PyMuPDF

# Load the SpaCy model
nlp = spacy.load('en_core_web_sm')

def process_recruiters_mode():
    st.title("Recruiter's Panel")

    # File upload for resumes
    uploaded_files = st.file_uploader("Upload resumes (PDF)", accept_multiple_files=True)
    
    # Input for required skills
    required_skills_input = st.text_input("Enter required skills (comma-separated)", "")
    required_skills = [skill.strip().lower() for skill in required_skills_input.split(',') if skill.strip()]
    
    # Button to save required skills to UpdatedSkills.csv
    if st.button("Save Required Skills"):
        save_required_skills(required_skills)

    # Check skills and extract names in uploaded resumes and collect all skills found
    all_skills_found = set()
    if uploaded_files:
        for file in uploaded_files:
            text = extract_text_from_pdf(file)
            doc = nlp(text)  # Convert text to a SpaCy doc object
            skills_found = extract_skills(doc, required_skills)
            display_candidate_info(file.name, required_skills, skills_found)

            all_skills_found.update(skills_found)

            # Call csv_skills with SpaCy doc object
            skills_from_csv = csv_skills(doc)
            display_skills_from_csv(file.name, skills_from_csv)

    # Filter overall skills to show only skills found in uploaded resumes
    overall_skills_filtered = all_skills_found.intersection(parse_all_skills())

    # Display filtered overall skills found across all resumes
    display_overall_skills(overall_skills_filtered)

    # Additional functionalities for shortlisting, comparisons, etc.
    # Add your recruiter-specific functionalities here

def save_required_skills(required_skills):
    with open('data/UpdatedSkills.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        for skill in required_skills:
            writer.writerow([skill])

# Function to extract text from PDF file
def extract_text_from_pdf(file):
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

# Function to extract skills based on provided keywords from CSV
def csv_skills(doc):
    skills_keywords = load_keywords('data/newSkills.csv')
    skills = set()

    for keyword in skills_keywords:
        if keyword.lower() in doc.text.lower():
            skills.add(keyword)

    return skills

# Function to load keywords from a CSV file
def load_keywords(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        keywords = [row[0] for row in reader]
    return keywords

# Function to extract skills using SpaCy Matcher
def extract_skills(doc, required_skills):
    matcher = Matcher(nlp.vocab)
    skills_found = set()

    for skill in required_skills:
        pattern = [{"LOWER": skill}]
        matcher.add(skill, [pattern])

    matches = matcher(doc)
    for match_id, start, end in matches:
        matched_skill = doc[start:end].text.lower()
        skills_found.add(matched_skill)

    return skills_found

# Function to parse all skills from UpdatedSkills.csv
def parse_all_skills():
    skills_list = set()
    with open('data/UpdatedSkills.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            for item in row:
                skills_list.add(str(item).lower())
    
    return skills_list

# Function to display candidate information
def display_candidate_info(file_name, required_skills, skills_found):
    st.write("-" * 30)
    st.write(f"**Candidate Name:** {file_name}")
    st.write("**Skills found or not section:**")
    for skill in required_skills:
        if skill in skills_found:
            st.write(f"- {skill}: Found")
        else:
            st.write(f"- {skill}: Not Found")
    
    # Display all parsed skills found in the resume
    parsed_skills = sorted(list(skills_found))
    st.write("\n**All Skills from resume:**")
    for parsed_skill in parsed_skills:
        st.write(f"- {parsed_skill}")
    st.write("-" * 30)

# Function to display skills from CSV
def display_skills_from_csv(file_name, skills_from_csv):
    st.write(f"Skills from CSV found in {file_name}: {', '.join(skills_from_csv)}")

# Function to display overall skills
def display_overall_skills(overall_skills):
    st.write("\n**Overall Skills Found:**")
    for skill in overall_skills:
        st.write(f"- {skill}")

if __name__ == "__main__":
    process_recruiters_mode()
