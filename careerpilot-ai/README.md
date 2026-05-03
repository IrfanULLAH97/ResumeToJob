# CareerPilot AI – Resume-to-Job Match & Application Assistant

CareerPilot AI is a Generative AI-powered career assistant that helps users upload a PDF resume, extract skills, match with jobs, identify missing skills, and generate resume feedback and cover letters.

## Problem Statement

Many students and fresh graduates apply randomly without knowing which jobs actually match their skills. Traditional job portals mostly provide keyword search, but they usually do not explain skill gaps or provide personalized application guidance.

## Solution

CareerPilot AI combines resume text extraction, skill matching, job comparison, and Generative AI to help users understand where they fit best. It provides match scores, missing skills, resume improvement suggestions, and tailored cover letters for selected roles.

## Features

- PDF resume upload
- Manual resume paste option
- Resume text extraction
- Skill detection
- Job match scoring
- Missing skill analysis
- AI resume feedback
- AI cover letter generation
- Downloadable cover letter

## Tech Stack

- Python
- Streamlit
- pdfplumber
- Gemini API
- JSON job dataset

## Project Structure

```text
careerpilot-ai/
├── app.py
├── jobs.json
├── requirements.txt
├── README.md
├── .env.example
├── utils/
│   ├── __init__.py
│   ├── ai_helper.py
│   ├── job_api.py
│   ├── job_matcher.py
│   └── pdf_reader.py
└── assets/
    └── screenshots/
```

## How to Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit app:

```bash
streamlit run app.py
```

## Environment Variables

Create a `.env` file in the project root and add:

```env
GEMINI_API_KEY=your_api_key_here
```

This key is used for AI-powered resume feedback and cover letter generation.

## Demo Flow

1. Upload a resume PDF or paste resume text manually.
2. Click `Analyze Resume`.
3. View detected skills.
4. Review matched job roles and match scores.
5. Select a job for AI feedback.
6. Generate resume feedback.
7. Generate a tailored cover letter.
8. Download the cover letter as a `.txt` file.

## Limitations

- Works best with text-based PDFs.
- Scanned PDFs may still need improved OCR support for the best results.
- The MVP primarily relies on a sample-based local job dataset.

## Future Improvements

- Real job API integration
- OCR for scanned resumes
- LinkedIn profile analysis
- Resume PDF improvement generator
- Interview question generator
- Dashboard analytics

## Team

- Muhammad Ahsan: https://github.com/mAhsan0553
