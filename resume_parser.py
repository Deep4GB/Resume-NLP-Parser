import re
import fitz
import base64
import streamlit as st
import spacy
import csv
import nltk

# Additional libraries
nltk.download('punkt')

# Load the spaCy model for English
nlp = spacy.load('en_core_web_sm')

def load_keywords(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        return set(row[0] for row in reader)

# ----------------------------------Extract Name----------------------------------
def extract_name(doc):
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            names = ent.text.split()
            if len(names) >= 2 and names[0].istitle() and names[1].istitle():
                return names[0], ' '.join(names[1:])
    return "", ""
# --------------------------------------------------------------------------------

# ----------------------------------Extract Email---------------------------------
def extract_email(doc):
    matcher = spacy.matcher.Matcher(nlp.vocab)
    email_pattern = [{'LIKE_EMAIL': True}]
    matcher.add('EMAIL', [email_pattern])

    matches = matcher(doc)
    for match_id, start, end in matches:
        if match_id == nlp.vocab.strings['EMAIL']:
            return doc[start:end].text
    return ""
# --------------------------------------------------------------------------------

# ----------------------------------Extract Ph No---------------------------------
def extract_contact_number_from_resume(doc):
    contact_number = None
    text = doc.text  # Extract text from SpaCy doc object
    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    match = re.search(pattern, text)
    if match:
        contact_number = match.group()
    return contact_number
# --------------------------------------------------------------------------------

# --------------------------------Extract Education-------------------------------
def extract_education_from_resume(doc):
    universities = []

    # Process the document with spaCy
    doc = nlp(doc)

    # Iterate through entities and check for organizations (universities)
    for entity in doc.ents:
        if entity.label_ == "ORG" and ("university" in entity.text.lower() or "college" in entity.text.lower() or "institute" in entity.text.lower()):
            universities.append(entity.text)

    return universities
# --------------------------------------------------------------------------------

# ----------------------------------Extract Skills--------------------------------
def csv_skills(doc):
    skills_keywords = load_keywords('data/newSkills.csv')
    skills = set()

    for keyword in skills_keywords:
        if keyword.lower() in doc.text.lower():
            skills.add(keyword)

    return skills

nlp_skills = spacy.load('TrainedModel/skills')  # Load the trained NER model for skills

def extract_skills_from_ner(doc):
    non_skill_labels = {'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL', 'EMAIL'}
    
    skills = set()
    for ent in nlp_skills(doc.text).ents:
        if ent.label_ == 'SKILL':
            # Check if the entity text is not in the non-skill labels set
            if ent.label_ not in non_skill_labels and not ent.text.isdigit():
                # Filter out non-alphabetic characters
                skill_text = ''.join(filter(str.isalpha, ent.text))
                if skill_text:
                    skills.add(skill_text)
    return skills

def is_valid_skill(skill_text):
    # Define criteria for valid skills (modify/add criteria as needed)
    return len(skill_text) > 1 and not any(char.isdigit() for char in skill_text)

def extract_skills(doc):
    skills_csv = csv_skills(doc)
    skills_ner = extract_skills_from_ner(doc)
    
    filtered_skills_csv = {skill for skill in skills_csv if is_valid_skill(skill)}
    filtered_skills_ner = {skill for skill in skills_ner if is_valid_skill(skill)}
    
    combined_skills = filtered_skills_csv.union(filtered_skills_ner)  # Combine filtered skills without duplicates
    
    return list(combined_skills)  # Return combined filtered skills as a list

# --------------------------------------------------------------------------------

# ----------------------------------Extract Major---------------------------------
def extract_major(doc):
    major_keywords = load_keywords('data/majors.csv')

    for keyword in major_keywords:
        if keyword.lower() in doc.text.lower():
            return keyword

    return ""
# --------------------------------------------------------------------------------

# --------------------------------Extract Experience-------------------------------
def extract_experience(doc):
    verbs = [token.text for token in doc if token.pos_ == 'VERB']

    senior_keywords = ['lead', 'manage', 'direct', 'oversee', 'supervise', 'orchestrate', 'govern']
    mid_senior_keywords = ['develop', 'design', 'analyze', 'implement', 'coordinate', 'execute', 'strategize']
    mid_junior_keywords = ['assist', 'support', 'collaborate', 'participate', 'aid', 'facilitate', 'contribute']
    
    if any(keyword in verbs for keyword in senior_keywords):
        level_of_experience = "Senior"
    elif any(keyword in verbs for keyword in mid_senior_keywords):
        level_of_experience = "Mid-Senior"
    elif any(keyword in verbs for keyword in mid_junior_keywords):
        level_of_experience = "Mid-Junior"
    else:
        level_of_experience = "Entry Level"

    suggested_position = suggest_position(verbs)

    return {
        'level_of_experience': level_of_experience,
        'suggested_position': suggested_position
    }

# --------------------------------------------------------------------------------


# -----------------------------------Suggestions----------------------------------
def load_positions_keywords(file_path):
    positions_keywords = {}
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            position = row['position']
            keywords = [keyword.lower()
                        for keyword in row['keywords'].split(',')]
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
    return nlp(text)


def show_colored_skills(skills):
    st.write(', '.join(skills))


def calculate_resume_score(resume_info):
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


def extract_resume_info(doc):
    first_lines = '\n'.join(doc.text.splitlines()[:10])
    first_name, last_name = extract_name(doc)
    email = extract_email(doc)
    skills = extract_skills(doc)
    degree_major = extract_major(doc)
    experience = extract_experience(doc)

    return {'first_name': first_name, 'last_name': last_name, 'email': email, 'degree_major': degree_major, 'skills': skills, 'experience': experience}


def suggest_skills_for_job(desired_job):
    job_skills_mapping = {}
    
    with open('data/sugestedSkills.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            job_title = row[0].lower()
            skills = row[1:]
            job_skills_mapping[job_title] = skills
    
    desired_job_lower = desired_job.lower()
    if desired_job_lower in job_skills_mapping:
        suggested_skills = job_skills_mapping[desired_job_lower]
        return suggested_skills
    else:
        return []


'''
def show_pdf(uploaded_file):
    try:
        with open(uploaded_file.name, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    except AttributeError:
        base64_pdf = base64.b64encode(uploaded_file.read()).decode('utf-8')

    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

'''
