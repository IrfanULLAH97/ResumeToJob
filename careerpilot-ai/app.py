"""Main Streamlit app for CareerPilot AI."""

import json
from pathlib import Path

import streamlit as st

from utils.ai_helper import generate_cover_letter, generate_resume_feedback
from utils.job_api import fetch_remote_jobs
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


if "analysis_ready" not in st.session_state:
    st.session_state.analysis_ready = False
if "detected_skills" not in st.session_state:
    st.session_state.detected_skills = []
if "job_matches" not in st.session_state:
    st.session_state.job_matches = []
if "analyzed_resume_text" not in st.session_state:
    st.session_state.analyzed_resume_text = ""
if "resume_source" not in st.session_state:
    st.session_state.resume_source = ""
if "ai_resume_feedback" not in st.session_state:
    st.session_state.ai_resume_feedback = ""
if "ai_cover_letter" not in st.session_state:
    st.session_state.ai_cover_letter = ""
if "jobs_status_message" not in st.session_state:
    st.session_state.jobs_status_message = ""


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
    use_public_jobs = st.checkbox("Try fetching public jobs online")
    use_visa_sponsorship = st.checkbox(
        "Only show public jobs with visa sponsorship",
        disabled=not use_public_jobs,
        help="This filter is applied when public jobs are fetched from Arbeitnow.",
    )

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
        if uploaded_file is not None and pdf_error_message:
            st.warning(pdf_error_message)
        else:
            st.warning("Please upload a resume PDF or paste your resume text to begin the analysis.")
        st.session_state.analysis_ready = False
        st.session_state.detected_skills = []
        st.session_state.job_matches = []
        st.session_state.analyzed_resume_text = ""
        st.session_state.resume_source = ""
        st.session_state.ai_resume_feedback = ""
        st.session_state.ai_cover_letter = ""
    else:
        detected_skills = extract_skills(resume_text)
        st.session_state.analyzed_resume_text = resume_text
        st.session_state.resume_source = (
            "PDF extraction" if extracted_resume_text else "Manual text input"
        )
        st.session_state.ai_resume_feedback = ""
        st.session_state.ai_cover_letter = ""
        st.session_state.jobs_status_message = ""

        if detected_skills:
            st.session_state.detected_skills = detected_skills
            jobs = load_jobs()

            if use_public_jobs:
                remote_jobs = fetch_remote_jobs(
                    visa_sponsorship=use_visa_sponsorship,
                )
                if remote_jobs:
                    jobs.extend(remote_jobs)
                    if use_visa_sponsorship:
                        st.session_state.jobs_status_message = (
                            f"Loaded {len(remote_jobs)} public jobs with visa sponsorship "
                            "in addition to local sample jobs."
                        )
                    else:
                        st.session_state.jobs_status_message = (
                            f"Loaded {len(remote_jobs)} public remote jobs in addition to local sample jobs."
                        )
                else:
                    st.session_state.jobs_status_message = "Using local sample jobs for demo."

            st.session_state.job_matches = match_resume_to_jobs(detected_skills, jobs)
            st.session_state.analysis_ready = True
        else:
            st.session_state.detected_skills = []
            st.session_state.job_matches = []
            st.session_state.analysis_ready = False
            st.session_state.jobs_status_message = ""
            st.warning(
                "No skills were detected. Please paste a more detailed resume with tools, "
                "technologies, coursework, or project experience."
            )

with right_column:
    st.markdown("### Detected Skills")
    if st.session_state.detected_skills:
        st.markdown(render_skill_badges(st.session_state.detected_skills))
    else:
        st.caption("Your detected skills and resume summary will appear here after analysis.")

    st.markdown("### Resume Summary")
    if st.session_state.analysis_ready:
        st.markdown(f"**Total detected skills:** {len(st.session_state.detected_skills)}")
        st.markdown(f"**Resume source:** {st.session_state.resume_source}")
    else:
        st.caption("Provide a resume to see skill detection and matching insights.")

if st.session_state.analysis_ready and st.session_state.job_matches:
    st.markdown("## Job Matches")
    st.markdown("### Top Job Matches")

    if st.session_state.jobs_status_message:
        st.info(st.session_state.jobs_status_message)

    for job in st.session_state.job_matches:
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
                if job.get("url"):
                    st.markdown(f"[Apply]({job['url']})")

            with score_col:
                st.markdown(f"### {job['match_score']}%")
                st.progress(job["match_score"] / 100)
                st.markdown(f"**{job['match_label']}**")

            st.markdown("**Matched Skills**")
            st.markdown(render_skill_badges(job["matched_skills"]))

            st.markdown("**Missing Skills**")
            st.markdown(render_skill_badges(job["missing_skills"]))

    st.markdown("## AI Assistance")
    job_option_labels = [
        f"{job['title']} | {job['company']} | {job['match_score']}%"
        for job in st.session_state.job_matches
    ]
    selected_job_label = st.selectbox(
        "Select a job for AI feedback",
        options=job_option_labels,
        index=None,
        placeholder="Choose a matched job",
    )

    selected_job = None
    if selected_job_label:
        selected_job = next(
            (
                job for job in st.session_state.job_matches
                if f"{job['title']} | {job['company']} | {job['match_score']}%"
                == selected_job_label
            ),
            None,
        )

    feedback_column, cover_letter_column = st.columns(2, gap="large")

    with feedback_column:
        generate_feedback = st.button(
            "Generate Resume Feedback",
            use_container_width=True,
        )

    with cover_letter_column:
        generate_letter = st.button(
            "Generate Cover Letter",
            use_container_width=True,
        )

    if generate_feedback:
        if not st.session_state.analyzed_resume_text.strip():
            st.warning("Please upload or paste resume text before requesting AI feedback.")
        elif not selected_job:
            st.warning("Please select a job for AI feedback.")
        else:
            with st.spinner("Generating AI resume feedback..."):
                st.session_state.ai_resume_feedback = generate_resume_feedback(
                    st.session_state.analyzed_resume_text,
                    selected_job,
                )

    if generate_letter:
        if not st.session_state.analyzed_resume_text.strip():
            st.warning("Please upload or paste resume text before generating a cover letter.")
        elif not selected_job:
            st.warning("Please select a job for AI feedback.")
        else:
            with st.spinner("Generating cover letter..."):
                st.session_state.ai_cover_letter = generate_cover_letter(
                    st.session_state.analyzed_resume_text,
                    selected_job,
                )

    if st.session_state.ai_resume_feedback:
        st.markdown("## AI Resume Feedback")
        st.write(st.session_state.ai_resume_feedback)

    if st.session_state.ai_cover_letter:
        st.markdown("## Generated Cover Letter")
        st.write(st.session_state.ai_cover_letter)
        st.download_button(
            "Download Cover Letter",
            data=st.session_state.ai_cover_letter,
            file_name="careerpilot_cover_letter.txt",
            mime="text/plain",
        )
