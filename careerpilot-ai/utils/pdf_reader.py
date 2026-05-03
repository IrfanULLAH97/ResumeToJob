"""Helpers for reading resume text from PDF files."""

import pdfplumber


def extract_text_from_pdf(uploaded_file):
    """
    Extract text from an uploaded PDF file.

    Parameters:
        uploaded_file: A file uploaded through Streamlit.

    Returns:
        tuple[str, str]:
            - extracted_text: Combined text from all PDF pages
            - error_message: Error details if reading fails, otherwise an empty string
    """
    if uploaded_file is None:
        return "", ""

    extracted_pages = []

    try:
        uploaded_file.seek(0)

        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    extracted_pages.append(page_text)

        extracted_text = "\n".join(extracted_pages).strip()
        return extracted_text, ""

    except Exception as error:
        error_message = f"Could not read the uploaded PDF: {error}"
        return "", error_message
