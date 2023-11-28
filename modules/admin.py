import base64
import sqlite3
import streamlit as st
import pandas as pd

def process_admin_mode():
    st.title("Admin Panel")
    st.subheader("Authentication Required")

    # Admin authentication
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")
    if st.button("Login"):
        if authenticate_admin(username, password):
            st.success("Authentication successful!")

            # Display uploaded PDFs in a table with download links and name fields
            display_uploaded_pdfs()

            st.markdown('---')
            
            # Display feedback data
            display_feedback_data()

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

        st.subheader("Latest Feedbacks")
        st.write(latest_feedback)  # Display latest 10 feedbacks

        if st.button("View More Feedbacks"):
            st.write(feedback_data)  # Display all feedbacks if requested by admin

    except FileNotFoundError:
        st.warning("No feedback data available.")

def get_uploaded_pdfs():
    try:
        conn = sqlite3.connect('data/user_pdfs.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM user_uploaded_pdfs")
        uploaded_pdfs = cursor.fetchall()
        conn.close()
        return uploaded_pdfs

    except sqlite3.Error as e:
        st.error(f"Error fetching uploaded PDFs: {e}")
        return []

def display_uploaded_pdfs():
    uploaded_pdfs = get_uploaded_pdfs()

    if uploaded_pdfs:
        st.subheader("Uploaded Resumes")

        pdf_data_list = []
        for pdf_id, pdf_name in uploaded_pdfs:
            pdf_data = get_pdf_data(pdf_id)
            if pdf_data:
                pdf_b64 = base64.b64encode(pdf_data[1]).decode('utf-8')
                href = f'<a href="data:application/pdf;base64,{pdf_b64}" download="{pdf_name}">Download</a>'
                pdf_data_list.append({"ID": pdf_id, "Name": pdf_name, "Download (Resume)": href})
            else:
                st.warning(f"Error retrieving PDF data for ID: {pdf_id}")

        # Create DataFrame from the list of dictionaries
        pdf_table = pd.DataFrame(pdf_data_list)
        # Display the table with HTML links using markdown
        st.markdown(pdf_table.to_html(escape=False), unsafe_allow_html=True)

    else:
        st.warning("No uploaded PDFs available.")

def get_pdf_data(pdf_id):
    try:
        conn = sqlite3.connect('data/user_pdfs.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, data FROM user_uploaded_pdfs WHERE id=?", (pdf_id,))
        pdf_data = cursor.fetchone()
        conn.close()
        return pdf_data

    except sqlite3.Error as e:
        st.error(f"Error fetching PDF data: {e}")
        return None

if __name__ == "__main__":
    process_admin_mode()
