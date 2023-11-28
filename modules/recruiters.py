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
            candidate_name = extract_candidate_name(doc)
            display_candidate_info(candidate_name, file.name)

            parsed_skills = extract_all_skills(doc)
            display_parsed_skills(parsed_skills)

            skills_found = extract_skills(doc, required_skills)
            display_skills_found(required_skills, skills_found)

            all_skills_found.update(skills_found)

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

# Function to extract candidate's full name using SpaCy
def extract_candidate_name(doc):
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            return ent.text
    return "Candidate name not found"

# Function to extract all skills from the resume
def extract_all_skills(doc):
    all_skills = set()
    for token in doc:
        if token.pos_ == 'NOUN' and token.text.isalpha() and len(token.text) > 1:
            all_skills.add(token.text.lower())
    return all_skills

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
def display_candidate_info(candidate_name, file_name):
    st.write("-" * 30)
    st.write(f"**File Name:** {file_name}")
    st.subheader(f"**Candidate Name:** {candidate_name}")

# Function to display parsed skills from the resume
def display_parsed_skills(parsed_skills):
    if parsed_skills:
        parsed_skills_str = ", ".join(parsed_skills)
        st.subheader("\n**All Skills Parsed from Resume:**")
        st.write(parsed_skills_str)
    else:
        st.subheader("\n**No Skills Parsed from Resume**")

# Function to display skills found or not
def display_skills_found(required_skills, skills_found):
    st.subheader("\n**Skills Found or Not Found:**\n")
    for skill in required_skills:
        if skill in skills_found:
            st.write(f"- {skill}: Found")
        else:
            st.write(f"- {skill}: Not Found")


if __name__ == "__main__":
    process_recruiters_mode()
