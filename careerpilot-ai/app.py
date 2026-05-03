"""Main Streamlit app for CareerPilot AI."""

import streamlit as st

from utils.job_matcher import extract_skills
from utils.pdf_reader import extract_text_from_pdf


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

extracted_resume_text = ""
pdf_error_message = ""

if uploaded_file is not None:
    extracted_resume_text, pdf_error_message = extract_text_from_pdf(uploaded_file)

    if pdf_error_message:
        st.warning(pdf_error_message)
    elif extracted_resume_text:
        with st.expander("View Extracted Resume Text"):
            st.text_area(
                "Extracted resume text",
                value=extracted_resume_text,
                height=250,
                disabled=True,
            )

st.markdown("### Or Paste Resume Text")
manual_resume_text = st.text_area(
    "Paste your resume content here",
    height=220,
    placeholder="Copy and paste your resume text here...",
)

resume_text = extracted_resume_text if extracted_resume_text else manual_resume_text

if st.button("Analyze Resume"):
    if not resume_text.strip():
        st.warning("Please upload a PDF resume or paste resume text to continue.")
    else:
        detected_skills = extract_skills(resume_text)

        st.markdown("### Detected Skills")

        if detected_skills:
            skill_badges = " ".join([f"`{skill}`" for skill in detected_skills])
            st.markdown(skill_badges)
        else:
            st.warning("No skills were detected in the provided resume text.")
