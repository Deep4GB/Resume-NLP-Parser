import streamlit as st
import spacy
from PyPDF2 import PdfReader

# Load the spaCy model for English
nlp = spacy.load('en_core_web_sm')

def extract_name(doc):
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            names = ent.text.split()
            if len(names) >= 2 and names[0].istitle() and names[1].istitle():
                return names[0], ' '.join(names[1:])
    return "", ""

def extract_skills(doc):
    skills = set()

    skill_pattern = [{"POS": "NOUN", "OP": "+"}]
    matcher = spacy.matcher.Matcher(nlp.vocab)
    matcher.add("Skills", [skill_pattern])

    matches = matcher(doc)
    for match_id, start, end in matches:
        skill_phrase = ' '.join([token.text for token in doc[start:end]])
        skills.add(skill_phrase)

    return skills

def extract_experience(doc):
    verbs = [token.text for token in doc if token.pos_ == 'VERB']

    if any(keyword in verbs for keyword in ['lead', 'manage', 'direct']):
        level_of_experience = "Senior"
    elif any(keyword in verbs for keyword in ['develop', 'design', 'analyze']):
        level_of_experience = "Mid-Senior"
    elif any(keyword in verbs for keyword in ['assist', 'support', 'collaborate']):
        level_of_experience = "Mid-Junior"
    else:
        level_of_experience = "Entry Level"

    return level_of_experience

def extract_text_from_pdf(uploaded_file):
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

def main():
    st.title("Resume Parser with NLP")

    uploaded_file = st.file_uploader("Upload a resume in PDF format", type=["pdf"])

    if uploaded_file is not None:
        text = extract_text_from_pdf(uploaded_file)
        doc = nlp(text)

        st.subheader("Parsed Resume Information:")
        
        # Extracting Name
        first_name, last_name = extract_name(doc)
        st.write(f"Name: {first_name} {last_name}")

        # Extracting Skills
        skills = extract_skills(doc)
        st.write("Skills:", ', '.join(skills) if skills else "No skills identified")

        # Extracting Experience
        experience = extract_experience(doc)
        st.write(f"Experience Level: {experience}")

if __name__ == "__main__":
    main()
