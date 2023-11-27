import pandas as pd
import streamlit as st
import sqlite3

# Function to create a database table if it doesn't exist
def create_resume_table():
    conn = sqlite3.connect('resume_database.db')
    c = conn.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS resumes (
                  id INTEGER PRIMARY KEY,
                  file_name TEXT,
                  file_path TEXT
              )''')
    conn.commit()
    conn.close()

def process_admin_mode():
    create_resume_table()
    st.title("Admin Panel")
    st.subheader("Authentication Required")

    # Admin authentication
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")
    if st.button("Login"):
        if authenticate_admin(username, password):
            st.success("Authentication successful!")

            # Display feedback data
            st.subheader("Feedback Data")
            display_feedback_data()

            # Display uploaded resumes
            display_uploaded_resumes()
        else:
            st.error("Authentication failed. Please try again.")

def authenticate_admin(username, password):
    # Replace this with your actual authentication logic
    hardcoded_username = "deep"
    hardcoded_password = "dp10"
    return username == hardcoded_username and password == hardcoded_password

def display_feedback_data():
    try:
        feedback_data = pd.read_csv('data/feedback_data.csv')
        latest_feedback = feedback_data.tail(10)  # Fetching latest 10 feedbacks

        st.write(latest_feedback)  # Display latest 10 feedbacks

        if st.button("View More Feedbacks"):
            st.write(feedback_data)  # Display all feedbacks if requested by admin
    except FileNotFoundError:
        st.warning("No feedback data available.")

def display_uploaded_resumes():
    conn = sqlite3.connect('resume_database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM resumes")
    resumes = c.fetchall()
    conn.close()

    st.subheader("Uploaded Resumes:")
    for resume in resumes:
        st.write(resume[1])  # Display file names
        download_button = st.button(f"Download {resume[1]}", key=f"download_button_{resume[0]}")
        if download_button:
            with open(resume[2], 'rb') as file:
                file_contents = file.read()
            st.download_button(label='Download Resume', data=file_contents, file_name=resume[1])

if __name__ == "__main__":
    process_admin_mode()
