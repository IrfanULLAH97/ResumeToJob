"""Helpers for extracting resume skills and future job matching."""

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


def calculate_match_score(resume_skills, job_description):
    """
    Compare detected resume skills with a job description.

    Returns:
        tuple: (score, matched_skills, missing_skills)
    """
    if not job_description:
        return 0, [], []

    job_text = job_description.lower()
    required_skills = [
        skill for skill in SKILL_LIST if re.search(_build_skill_pattern(skill), job_text)
    ]
    matched_skills = [skill for skill in resume_skills if skill in required_skills]
    missing_skills = [skill for skill in required_skills if skill not in resume_skills]

    if not required_skills:
        return 0, matched_skills, missing_skills

    score = int((len(matched_skills) / len(required_skills)) * 100)
    return score, matched_skills, missing_skills
