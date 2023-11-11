# feedback.py
import streamlit as st
import pandas as pd

# Assuming feedback_data is accessible globally or imported
feedback_data = pd.DataFrame(columns=['User Name', 'Feedback', 'Timestamp'])

def process_feedback_mode():
    st.title("Feedback Section")
    st.subheader("Provide Feedback")

    # Feedback Form
    user_name = st.text_input("Your Name:")
    feedback = st.text_area("Provide feedback on the resume parser:", height=100)
    if st.button("Submit Feedback"):
        feedback_data.loc[len(feedback_data)] = [user_name, feedback, pd.to_datetime("now")]
        st.success("Feedback submitted successfully!")
