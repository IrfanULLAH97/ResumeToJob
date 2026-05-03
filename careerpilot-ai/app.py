"""Main Streamlit app for CareerPilot AI."""

import streamlit as st


st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="C",
    layout="centered",
)


st.title("CareerPilot AI")
st.subheader("Resume-to-Job Match & Application Assistant")

st.write(
    """
    CareerPilot AI is a beginner-friendly Streamlit project that helps users
    upload a resume, compare it with job descriptions, and later receive
    AI-powered feedback for improving applications.
    """
)

st.markdown("### Upload Your Resume")
uploaded_file = st.file_uploader("Upload a PDF resume", type=["pdf"])

st.markdown("### Or Paste Resume Text")
resume_text = st.text_area(
    "Paste your resume content here",
    height=220,
    placeholder="Copy and paste your resume text here...",
)

if st.button("Analyze Resume"):
    st.info("Resume analysis will appear here.")
