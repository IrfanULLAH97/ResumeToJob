"""Main Streamlit app for CareerPilot AI."""

import json
from pathlib import Path

import streamlit as st

from utils.job_matcher import extract_skills, match_resume_to_jobs
from utils.pdf_reader import extract_text_from_pdf


st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🎯",
    layout="wide",
)


def load_jobs():
    """Load sample jobs from the local jobs.json file."""
    jobs_file = Path(__file__).parent / "jobs.json"

    try:
        with jobs_file.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def render_skill_badges(skills):
    """Render a simple badge-like row of skills using markdown."""
    if not skills:
        return "None"

    return " ".join([f"`{skill}`" for skill in skills])


with st.sidebar:
    st.title("CareerPilot AI")
    st.write(
        "An AI-powered assistant that helps turn resume text into clearer job-fit insights."
    )

    st.markdown("### Workflow")
    st.markdown(
        """
        1. Upload PDF resume
        2. Extract skills
        3. Match with jobs
        4. Generate AI feedback
        5. Generate cover letter
        """
    )

    st.markdown("### Tech Stack")
    st.markdown(
        """
        - Streamlit
        - Python
        - pdfplumber
        - JSON job dataset
        - Gemini-ready AI helpers
        """
    )


st.title("🎯 CareerPilot AI")
st.subheader("Resume-to-Job Match & Application Assistant")
st.write(
    """
    Many students and early-career professionals struggle to understand how well
    their resume matches real opportunities. CareerPilot AI helps turn resume
    content into detected skills and ranked job matches in one place.
    """
)

st.markdown("## Resume Input")

left_column, right_column = st.columns([1.2, 1], gap="large")

with left_column:
    st.markdown("### Upload or Paste Your Resume")
    uploaded_file = st.file_uploader("Upload a PDF resume", type=["pdf"])

with right_column:
    st.markdown("### Analysis Summary")
    st.info(
        "Upload a PDF or paste resume text on the left. CareerPilot AI will extract "
        "skills and compare them with sample jobs."
    )

extracted_resume_text = ""
pdf_error_message = ""

if uploaded_file is not None:
    extracted_resume_text, pdf_error_message = extract_text_from_pdf(uploaded_file)

with left_column:
    if pdf_error_message:
        st.warning(f"{pdf_error_message} Please paste your resume text manually instead.")
    elif uploaded_file is not None and extracted_resume_text:
        st.success("Resume text extracted successfully from the uploaded PDF.")
        with st.expander("View Extracted Resume Text"):
            st.text_area(
                "Extracted resume text",
                value=extracted_resume_text,
                height=250,
                disabled=True,
            )

    st.markdown("### Manual Resume Text")
    manual_resume_text = st.text_area(
        "Paste your resume content here",
        height=260,
        placeholder="Copy and paste your resume text here...",
    )

resume_text = extracted_resume_text if extracted_resume_text else manual_resume_text

analyze_resume = st.button("Analyze Resume", use_container_width=True)

st.markdown("## Analysis Results")

if analyze_resume:
    if not resume_text.strip():
        st.warning("Please upload a resume PDF or paste your resume text to begin the analysis.")
    else:
        detected_skills = extract_skills(resume_text)

        with right_column:
            st.markdown("### Detected Skills")

            if detected_skills:
                st.markdown(render_skill_badges(detected_skills))

                st.markdown("### Resume Summary")
                st.markdown(f"**Total detected skills:** {len(detected_skills)}")
                st.markdown(
                    f"**Resume source:** {'PDF extraction' if extracted_resume_text else 'Manual text input'}"
                )
            else:
                st.warning(
                    "No skills were detected. Please paste a more detailed resume with tools, "
                    "technologies, coursework, or project experience."
                )

        if detected_skills:
            job_matches = match_resume_to_jobs(detected_skills, load_jobs())

            st.markdown("## Job Matches")
            st.markdown("### Top Job Matches")

            for job in job_matches:
                expander_title = (
                    f"{job['title']} | {job['company']} | {job['match_score']}% Match"
                )

                with st.expander(expander_title):
                    info_col, score_col = st.columns([1.3, 1], gap="large")

                    with info_col:
                        st.markdown(f"**Company:** {job['company']}")
                        st.markdown(f"**Location:** {job['location']}")
                        st.markdown(f"**Category:** {job['category']}")
                        st.markdown(f"**Job Description:** {job['description']}")

                    with score_col:
                        st.markdown(f"### {job['match_score']}%")
                        st.progress(job["match_score"] / 100)
                        st.markdown(f"**{job['match_label']}**")

                    st.markdown("**Matched Skills**")
                    st.markdown(render_skill_badges(job["matched_skills"]))

                    st.markdown("**Missing Skills**")
                    st.markdown(render_skill_badges(job["missing_skills"]))
else:
    with right_column:
        st.markdown("### Detected Skills")
        st.caption("Your detected skills and resume summary will appear here after analysis.")
        st.markdown("### Resume Summary")
        st.caption("Provide a resume to see skill detection and matching insights.")
