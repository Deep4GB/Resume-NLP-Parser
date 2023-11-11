# admin.py
import streamlit as st

def process_admin_mode():
    st.title("Admin Panel")
    st.subheader("Authentication Required")

    # Admin authentication
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")
    if st.button("Login"):
        if authenticate_admin(username, password):
            st.success("Authentication successful!")

            # Admin functionalities go here

            # Display feedback data
            st.subheader("Feedback Data")
            # Assuming feedback_data is accessible globally or imported
            st.write(feedback_data)
        else:
            st.error("Authentication failed. Please try again.")

def authenticate_admin(username, password):
    # Replace this with your actual authentication logic
    hardcoded_username = "deep"
    hardcoded_password = "dp10"
    return username == hardcoded_username and password == hardcoded_password
