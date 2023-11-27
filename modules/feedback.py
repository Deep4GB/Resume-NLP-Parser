import streamlit as st
from datetime import datetime

def process_feedback_mode():
    st.title("Feedback Section")
    st.subheader("Provide Feedback")

    # Feedback Form
    user_name = st.text_input("Your Name:")
    feedback = st.text_area("Provide feedback on the resume parser:", height=100)
    if st.button("Submit Feedback"):
        add_feedback(user_name, feedback)
        st.success("Feedback submitted successfully!")

def add_feedback(user_name, feedback):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('data/feedback_data.csv', 'a') as file:
        file.write(f"User Name: {user_name}\n")
        file.write(f"Feedback: {feedback}\n")
        file.write(f"Timestamp: {timestamp}\n")
        file.write("-" * 50 + "\n")
