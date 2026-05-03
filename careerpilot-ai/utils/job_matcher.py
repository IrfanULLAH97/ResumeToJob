"""Helpers for extracting resume skills and matching them to jobs."""

import re


SKILL_LIST = [
    "Python",
    "SQL",
    "Excel",
    "Power BI",
    "Tableau",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "NLP",
    "Data Analysis",
    "Data Visualization",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Node.js",
    "Flask",
    "FastAPI",
    "Django",
    "Git",
    "GitHub",
    "APIs",
    "Linux",
    "Docker",
    "AWS",
    "Azure",
    "Google Cloud",
    "Cybersecurity",
    "Network Security",
    "SCADA",
    "PLC",
    "DCS",
    "OT Security",
    "Problem Solving",
    "Communication",
    "Teamwork",
    "Leadership",
]


def _build_skill_pattern(skill: str) -> str:
    """Build a safe case-insensitive regex pattern for a skill."""
    skill_pattern = re.escape(skill.lower()).replace(r"\ ", r"\s+")
    return rf"(?<!\w){skill_pattern}(?!\w)"


def extract_skills(text: str) -> list:
    """
    Extract skills from resume text using a predefined skill list.

    Matching is case-insensitive and avoids duplicate results.
    """
    if not text:
        return []

    matched_skills = []

    for skill in SKILL_LIST:
        # Allow flexible spacing for multi-word skills while keeping matching safe
        # for short skills such as SQL, CSS, and AWS.
        pattern = _build_skill_pattern(skill)

        if re.search(pattern, text.lower()):
            matched_skills.append(skill)

    return matched_skills


def _unique_skills(skills: list) -> list:
    """Remove duplicates while preserving the original skill names and order."""
    unique_items = []
    seen_skills = set()

    for skill in skills or []:
        if not isinstance(skill, str):
            continue

        normalized_skill = skill.strip().lower()
        if not normalized_skill or normalized_skill in seen_skills:
            continue

        seen_skills.add(normalized_skill)
        unique_items.append(skill.strip())

    return unique_items


def _get_match_label(match_score: int) -> str:
    """Return a human-friendly label for a job match score."""
    if match_score >= 90:
        return "Excellent Match"
    if match_score >= 70:
        return "Good Match"
    if match_score >= 50:
        return "Moderate Match"
    return "Needs Improvement"


def match_resume_to_jobs(resume_skills: list, jobs: list) -> list:
    """
    Match resume skills against a list of jobs.

    Returns:
        list: Sorted job match dictionaries from highest score to lowest.
    """
    normalized_resume_skills = {
        skill.lower(): skill for skill in _unique_skills(resume_skills)
    }

    job_matches = []

    for job in jobs or []:
        required_skills = _unique_skills(job.get("required_skills", []))
        matched_skills = []
        missing_skills = []

        for required_skill in required_skills:
            if required_skill.lower() in normalized_resume_skills:
                matched_skills.append(required_skill)
            else:
                missing_skills.append(required_skill)

        if required_skills:
            match_score = round((len(matched_skills) / len(required_skills)) * 100)
        else:
            match_score = 0

        job_matches.append(
            {
                "id": job.get("id"),
                "title": job.get("title", "Untitled Role"),
                "company": job.get("company", "Unknown Company"),
                "location": job.get("location", "Not specified"),
                "category": job.get("category", "General"),
                "description": job.get("description", ""),
                "required_skills": required_skills,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "match_score": match_score,
                "match_label": _get_match_label(match_score),
            }
        )

    return sorted(job_matches, key=lambda job: job["match_score"], reverse=True)
