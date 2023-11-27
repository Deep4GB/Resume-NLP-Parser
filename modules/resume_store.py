import streamlit as st
import sqlite3
import os

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

# Function to store uploaded resumes in the database
def store_resume(file):
    conn = sqlite3.connect('resume_database.db')
    c = conn.cursor()
    c.execute("INSERT INTO resumes (file_name, file_path) VALUES (?, ?)", (file.name, f"resumes/{file.name}"))
    conn.commit()
    conn.close()
    with open(os.path.join("resumes", file.name), "wb") as f:
        f.write(file.getbuffer())

def process_admin_mode():
    create_resume_table()
    st.title("Admin Panel")
    st.subheader("Authentication Required")

    # Admin authentication
    # (Add authentication code here)

    # Display uploaded resumes and allow admin to download them
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

def process_user_mode():
    st.title("Resume Parser using NLP")
    uploaded_file = st.file_uploader("Upload a PDF resume", type="pdf")

    if uploaded_file:
        st.write("File uploaded successfully!")
        store_resume(uploaded_file)

def main():
    st.title("Resume Store Application")

    # Determine the mode (admin or user)
    mode_selection = st.radio("Select Mode:", ("User Mode", "Admin Mode"))

    if mode_selection == "User Mode":
        process_user_mode()
    elif mode_selection == "Admin Mode":
        process_admin_mode()

if __name__ == "__main__":
    main()
