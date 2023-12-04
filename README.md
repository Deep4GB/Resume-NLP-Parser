<center>

# Resume Parser Using NLP

</center>

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [How to Run the Application](#how-to-run-the-application)
- [Functionalities](#functionalities)
  - [User](#user)
  - [Recruiters](#recruiters)
  - [Feedback](#feedback)
  - [Admin](#admin)
- [Future Enhancements](#future-enhancements)
- [Team](#team)

## Overview

The **Resume NLP Parser** revolutionizes the recruitment process by employing sophisticated Natural Language Processing (NLP) techniques. This tool efficiently extracts, analyzes, and visualizes data from resumes, enabling data-driven decision-making in hiring. Tailored for both candidates and recruiters, it enhances the application experience by parsing resumes comprehensively and offering powerful insights.

## Key Features

- **Comprehensive Resume Parsing**: Extracts detailed information including contact details, skills, work experience, and educational background from resumes in PDF formats.

- **Advanced NLP Analysis**: Utilizes leading-edge NLP libraries such as NLTK and spaCy to delve into resume text, identifying keywords, phrases, and patterns to evaluate candidates' qualifications comprehensively.

- **Intuitive Data Visualization**: Presents parsed data through interactive visualizations, empowering recruiters with efficient insights into applicants' profiles.

- **Robust Search and Filtering**: Offers powerful search and filtering functionalities, enabling swift access to specific candidate information.

## Technologies Used

The project leverages the following technologies and tools:

- **Python**: Primary programming language for NLP, data analysis, and backend functionalities.
- **NLP Libraries**: Utilizes NLTK and spaCy for text analysis, named entity recognition (NER), and text parsing.
- **Web Interface**: Employs Streamlit to create a user-friendly web-based interface for seamless user interaction.
- **Data Visualization**: Utilizes Matplotlib and Plotly for generating informative and interactive visualizations.
- **Database Management**: Utilizes SQLite for efficiently managing and querying resume data.
- **Model Training**: Incorporates spaCy's NER pipeline for training models on customized data for skill extraction.

## How to Run the Application

To run the Resume NLP Parser:

1. Clone this repository to your local machine and ``cd`` into the project directory.
    ``` bash
    git@github.com:Deep4GB/Resume-NLP-Parser.git
    cd Resume-NLP-Parser
    ```
2. Set up a Python environment with necessary dependencies listed in `requirements.txt`.
    ``` bash
    pip install -r requirements.txt
    ```
3. Run the application using Streamlit:
    ```bash
    streamlit run main.py
    ```
4. Upload resumes and explore the parsed data using the application's functionalities.

## Functionalities

### User

The User section allows individuals to upload their resumes. The system then extracts and displays parsed information, showcasing extracted details such as skills, work experience, education, and contact information.

### Recruiters

Recruiters can upload multiple resumes and specify desired skills. The system performs skill-based searching across the resumes, presenting the findings in a structured format for better evaluation.

### Feedback

This section enables users to provide feedback, suggestions, or improvements for the system's enhancement. Users can share their thoughts on improving parsing accuracy, user interface, or additional functionalities.

### Admin

Admins have privileged access, requiring authentication to access this section. They can review uploaded resumes, manage feedback received from users, and download uploaded resumes for further analysis or archiving.

## Future Enhancements

In the pipeline for this project are several enhancements:

- **Machine Learning Integration**: Integrate machine learning algorithms to enhance resume analysis and categorization.
- **Customization Features**: Offer customization options for tailoring parsing algorithms to specific job roles or industries.
- **Database Integration and Management**: Implement a more robust database system for long-term storage and efficient data retrieval.

## Team

- **Darsh Patel**: [GitHub Profile](https://github.com/darsh8692)
- **Dev Patel**: [GitHub Profile](https://github.com/Devv64bit)
- **Deep Patel**: [GitHub Profile](https://github.com/Deep4GB)
- **Dravya Patel**: [GitHub Profile](https://github.com/dravyaaa)

