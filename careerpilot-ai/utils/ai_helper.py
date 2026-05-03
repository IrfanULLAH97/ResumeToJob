"""Helper functions for Gemini-powered resume feedback and cover letters."""

import os

import google.generativeai as genai
from dotenv import load_dotenv


GEMINI_MODEL_NAME = "gemini-2.5-flash"
MISSING_API_KEY_MESSAGE = (
    "Gemini API key is missing. Please add GEMINI_API_KEY in your .env file."
)


def configure_gemini():
    """
    Load the Gemini API key from the environment and configure the SDK.

    Returns:
        bool: True if the API key exists, otherwise False.
    """
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY", "").strip()

    if not api_key:
        return False

    genai.configure(api_key=api_key)
    return True


def _build_job_context(job: dict) -> str:
    """Convert a job dictionary into compact prompt context."""
    if not job:
        return "No job details were provided."

    required_skills = ", ".join(job.get("required_skills", [])) or "Not specified"

    return (
        f"Job Title: {job.get('title', 'Not specified')}\n"
        f"Company: {job.get('company', 'Not specified')}\n"
        f"Location: {job.get('location', 'Not specified')}\n"
        f"Category: {job.get('category', 'Not specified')}\n"
        f"Required Skills: {required_skills}\n"
        f"Description: {job.get('description', 'Not specified')}"
    )


def _generate_text(prompt: str) -> str:
    """Generate text from Gemini with graceful error handling."""
    if not configure_gemini():
        return MISSING_API_KEY_MESSAGE

    try:
        model = genai.GenerativeModel(model_name=GEMINI_MODEL_NAME)
        response = model.generate_content(prompt)
        response_text = getattr(response, "text", "")

        if response_text:
            return response_text.strip()

        return "Gemini did not return any text. Please try again with more detailed input."
    except Exception as error:
        return f"Could not generate AI content right now: {error}"


def generate_resume_feedback(resume_text: str, job: dict) -> str:
    """
    Generate resume feedback tailored to a selected job.
    """
    if not resume_text.strip():
        return "Please provide resume text before requesting resume feedback."

    prompt = f"""
You are a professional career advisor helping a student or early-career candidate.

Analyze the resume against the selected job and return a clear, practical response
with the following sections:
1. Overall suitability
2. Resume strengths
3. Missing skills/keywords
4. Specific resume improvement suggestions
5. Recommended learning focus

Keep the feedback honest, constructive, and concise. Do not invent experience.

Resume:
{resume_text}

Selected Job:
{_build_job_context(job)}
"""

    return _generate_text(prompt)


def generate_cover_letter(resume_text: str, job: dict) -> str:
    """
    Generate a short professional cover letter tailored to a selected job.
    """
    if not resume_text.strip():
        return "Please provide resume text before requesting a cover letter."

    prompt = f"""
Write a professional cover letter for a student or early-career candidate.

Requirements:
- Keep it short and clear
- Tailor it to the selected job
- Use only the information available in the resume and job description
- Do not add fake experience, achievements, or tools
- Keep the tone confident, realistic, and professional

Resume:
{resume_text}

Selected Job:
{_build_job_context(job)}
"""

    return _generate_text(prompt)
