1. **Name Extraction using spaCy:**
   - The `extract_name` function uses spaCy's English language model (`en_core_web_sm`) to process the first lines of the resume.
   - spaCy's named entity recognition (NER) is applied to identify entities in the text.
   - Specifically, it looks for entities labeled as 'PERSON' to extract the candidate's name.

2. **Email Extraction using spaCy:**
   - The `extract_email` function employs spaCy's matcher to find patterns resembling email addresses.
   - It defines a pattern for email recognition and uses the matcher to identify and extract email addresses from the resume.

3. **Skills Extraction using Keywords:**
   - The `extract_skills` function loads a set of keywords from a CSV file (`newSkills.csv`).
   - It then checks if these keywords are present in the resume text, irrespective of the case.
   - Keywords related to skills are added to a set, representing the skills possessed by the candidate.

4. **Degree/Major Extraction using Keywords:**
   - Similar to skills extraction, the `extract_major` function loads keywords related to majors from a CSV file (`majors.csv`).
   - It checks if these major-related keywords are present in the resume text and extracts the first match as the degree major.

5. **Verbs Extraction for Experience Analysis:**
   - The main function uses spaCy to process the entire resume text (`nlp(resume_text)`).
   - It extracts verbs (action words) from the text by filtering tokens with the part-of-speech tag 'VERB'.
   - These extracted verbs are then used to analyze the level of experience.

6. **Experience Analysis using Verbs:**
   - The `extract_experience` function analyzes the extracted verbs to determine the level of experience.
   - It checks for specific keywords ('lead', 'manage', 'develop', 'assist', etc.) in the list of verbs.
   - Based on the presence of these keywords, it categorizes the level of experience as 'Senior', 'Mid-Senior', 'Mid-Junior', or 'Entry Level'.

7. **Suggested Position using NLP:**
   - The `suggest_position` function leverages NLP by comparing the extracted verbs with predefined keywords for various positions.
   - It loads position-keywords mappings from a CSV file (`positions.csv`) and suggests a position based on the match.

8. **Name Entity Recognition (NER) for Position Suggestions:**
   - While suggesting positions, the program uses spaCy's NER to identify entities in the resume text.
   - Specifically, it looks for entities labeled as 'ORG' (organization) to enhance the accuracy of position suggestions.

9. **User Interaction and Display:**
   - The extracted information, including name, email, skills, degree/major, and experience details, is presented to the user through the Streamlit interface.

10. **Score Calculation based on Extracted Information:**
    - The `calculate_resume_score` function assigns scores based on the presence of critical information such as name, email, degree, and skills.

11. **Suggested Skills for Desired Job using NLP:**
    - The `suggest_skills_for_job` function suggests skills based on the desired job entered by the user.
    - It looks up predefined mappings of jobs to skills using NLP to enhance relevance.

