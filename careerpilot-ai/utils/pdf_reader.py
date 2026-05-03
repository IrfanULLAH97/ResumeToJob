"""Helpers for reading resume text from PDF files."""

import pdfplumber


def extract_text_from_pdf(uploaded_file):
    """
    Extract text from an uploaded PDF file.

    Parameters:
        uploaded_file: A file uploaded through Streamlit.

    Returns:
        str: Combined text from all PDF pages.
    """
    if uploaded_file is None:
        return ""

    extracted_pages = []

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_pages.append(page_text)

    return "\n".join(extracted_pages)
