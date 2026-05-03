"""Placeholder AI helper functions for future Gemini integration."""

import os

from dotenv import load_dotenv


load_dotenv()


def get_gemini_api_key():
    """Return the Gemini API key from environment variables."""
    return os.getenv("GEMINI_API_KEY", "")


def generate_resume_feedback(resume_text, job_description):
    """
    Placeholder function for future AI-generated feedback.

    Later, this function can call the Gemini API and generate tailored
    feedback based on the resume and job description.
    """
    if not resume_text or not job_description:
        return "Add resume text and a job description to generate feedback later."

    return "AI resume feedback will be generated here in a future version."


def generate_cover_letter(resume_text, job_description):
    """
    Placeholder function for future AI cover letter generation.
    """
    if not resume_text or not job_description:
        return "Add resume text and a job description to generate a cover letter later."

    return "AI cover letter generation will be added here in a future version."
