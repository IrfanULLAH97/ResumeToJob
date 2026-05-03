# CareerPilot AI

CareerPilot AI is a simple Streamlit project for matching resumes to job
descriptions.

## Features

- Upload a PDF resume
- Paste resume text manually
- Analyze resumes against sample job descriptions
- Placeholder support for future AI feedback and cover letter generation

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
│   ├── pdf_reader.py
│   ├── job_matcher.py
│   └── ai_helper.py
└── assets/
    └── screenshots/
```

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and add your Gemini API key if you want to use
   AI features later.
4. Run the app:

```bash
streamlit run app.py
```

## Notes

- This version is intentionally beginner-friendly.
- The current `Analyze Resume` button shows a placeholder message.
- Utility modules are included so you can expand the project step by step.
