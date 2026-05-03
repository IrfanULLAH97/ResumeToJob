"""Optional public job API integration for CareerPilot AI."""

import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from utils.job_matcher import extract_skills


REMOTIVE_API_URL = "https://remotive.com/api/remote-jobs"
ARBEITNOW_API_URL = "https://www.arbeitnow.com/api/job-board-api"
REQUEST_HEADERS = {
    "User-Agent": "CareerPilot-AI/1.0",
    "Accept": "application/json",
}


def fetch_remote_jobs(keyword="data", location="remote") -> list:
    """
    Fetch public remote jobs from a no-auth API source.

    Returns:
        list: Normalized job dictionaries. Returns an empty list if all APIs fail.
    """
    remotive_jobs = _fetch_remotive_jobs(keyword=keyword, location=location)
    if remotive_jobs:
        return remotive_jobs

    return _fetch_arbeitnow_jobs(keyword=keyword, location=location)


def _fetch_remotive_jobs(keyword="data", location="remote") -> list:
    """Fetch jobs from Remotive and normalize them."""
    query_params = {
        "search": keyword,
        "limit": 10,
    }

    try:
        request_url = f"{REMOTIVE_API_URL}?{urlencode(query_params)}"
        request = Request(request_url, headers=REQUEST_HEADERS)

        with urlopen(request, timeout=10) as response:
            payload = json.load(response)

        remote_jobs = []

        for job in payload.get("jobs", []):
            description = job.get("description", "") or ""
            tags = job.get("tags", []) or []
            combined_text = " ".join(
                [
                    job.get("title", ""),
                    description,
                    " ".join(tags),
                ]
            )

            remote_jobs.append(
                {
                    "id": f"remote-{job.get('id', len(remote_jobs) + 1)}",
                    "title": job.get("title", "Remote Role"),
                    "company": job.get("company_name", "Unknown Company"),
                    "location": location if location else job.get("candidate_required_location", "Remote"),
                    "category": job.get("category", "Remote Jobs"),
                    "required_skills": extract_skills(combined_text),
                    "description": _clean_description(description),
                }
            )

        return remote_jobs
    except Exception:
        return []


def _fetch_arbeitnow_jobs(keyword="data", location="remote") -> list:
    """Fetch jobs from Arbeitnow and normalize them."""
    query_params = {
        "search": keyword,
    }

    try:
        request_url = f"{ARBEITNOW_API_URL}?{urlencode(query_params)}"
        request = Request(request_url, headers=REQUEST_HEADERS)

        with urlopen(request, timeout=10) as response:
            payload = json.load(response)

        remote_jobs = []

        for job in payload.get("data", [])[:10]:
            description = job.get("description", "") or ""
            tags = job.get("tags", []) or []
            combined_text = " ".join(
                [
                    job.get("title", ""),
                    description,
                    " ".join(tags),
                ]
            )

            remote_jobs.append(
                {
                    "id": f"arbeitnow-{job.get('slug', len(remote_jobs) + 1)}",
                    "title": job.get("title", "Remote Role"),
                    "company": job.get("company_name", "Unknown Company"),
                    "location": job.get("location", location or "Remote"),
                    "category": "Remote Jobs",
                    "required_skills": extract_skills(combined_text),
                    "description": _clean_description(description),
                }
            )

        return remote_jobs
    except Exception:
        return []


def _clean_description(description: str) -> str:
    """Convert a long HTML-like description into a short readable summary."""
    if not description:
        return "Remote job imported from a public API."

    plain_text = description.replace("<br>", " ").replace("<br/>", " ").replace("<br />", " ")
    plain_text = " ".join(plain_text.split())

    return plain_text[:280] + "..." if len(plain_text) > 280 else plain_text
