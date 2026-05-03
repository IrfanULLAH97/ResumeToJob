"""Helpers for simple resume-to-job matching."""


def detect_skills(resume_text):
    """
    Detect basic skills from resume text using a small keyword list.

    This is a placeholder implementation designed to be easy to understand.
    """
    if not resume_text:
        return []

    known_skills = [
        "python",
        "javascript",
        "react",
        "html",
        "css",
        "sql",
        "git",
        "excel",
        "apis",
        "debugging",
        "communication",
        "teamwork",
    ]

    text_lower = resume_text.lower()
    matched_skills = [skill for skill in known_skills if skill in text_lower]
    return matched_skills


def calculate_match_score(resume_skills, job_description):
    """
    Compare detected resume skills with a job description.

    Returns:
        tuple: (score, matched_skills, missing_skills)
    """
    if not job_description:
        return 0, [], []

    job_text = job_description.lower()
    job_keywords = [
        "python",
        "javascript",
        "react",
        "html",
        "css",
        "sql",
        "git",
        "excel",
        "apis",
        "debugging",
        "communication",
        "teamwork",
    ]

    required_skills = [skill for skill in job_keywords if skill in job_text]
    matched_skills = [skill for skill in resume_skills if skill in required_skills]
    missing_skills = [skill for skill in required_skills if skill not in resume_skills]

    if not required_skills:
        return 0, matched_skills, missing_skills

    score = int((len(matched_skills) / len(required_skills)) * 100)
    return score, matched_skills, missing_skills
