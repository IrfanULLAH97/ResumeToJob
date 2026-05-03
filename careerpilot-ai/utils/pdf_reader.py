"""Helpers for reading resume text from PDF files."""

import importlib.util
import io
import os
import shutil
import tempfile

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
        pdf_bytes = _read_uploaded_file_bytes(uploaded_file)
        if not pdf_bytes:
            return "", "The uploaded PDF appears to be empty or could not be read."

        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    extracted_pages.append(page_text)

        extracted_text = "\n".join(extracted_pages).strip()

        if extracted_text:
            return extracted_text, ""

        # Some resumes are exported as image-based PDFs with no selectable text.
        ocr_text = _extract_text_with_ocr(pdf_bytes)
        if ocr_text:
            return ocr_text, ""

        return "", (
            "No selectable text was found in this PDF. It may be a scanned or image-based "
            "resume. Please paste the resume text manually or use an OCR-enabled PDF."
        )

    except Exception as error:
        error_message = f"Could not read the uploaded PDF: {error}"
        return "", error_message


def _extract_text_with_ocr(pdf_bytes):
    """
    Try OCR extraction for image-based PDFs when optional OCR dependencies exist.

    This stays optional so the app still works without extra system setup.
    """
    if not _ocr_is_available():
        return ""

    import pypdfium2 as pdfium
    import pytesseract

    tesseract_path = _find_tesseract_path()
    if tesseract_path:
        pytesseract.pytesseract.tesseract_cmd = tesseract_path

    try:
        ocr_text = _extract_text_with_ocr_from_pdfium(pdfium.PdfDocument(pdf_bytes))
        if ocr_text:
            return ocr_text
    except Exception:
        pass

    # Retry using a temporary file path. This is slightly more tolerant with
    # some PDFs and keeps the app reliable across different runtime contexts.
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(pdf_bytes)
            temp_pdf_path = temp_file.name

        try:
            ocr_text = _extract_text_with_ocr_from_pdfium(pdfium.PdfDocument(temp_pdf_path))
            if ocr_text:
                return ocr_text
        finally:
            if os.path.exists(temp_pdf_path):
                os.remove(temp_pdf_path)
    except Exception:
        return ""

    return ""


def _extract_text_with_ocr_from_pdfium(pdf_document):
    """Render PDF pages to images and run OCR on them."""
    import pytesseract

    extracted_pages = []

    for page_index in range(len(pdf_document)):
        page = pdf_document[page_index]
        bitmap = page.render(scale=3)
        image = bitmap.to_pil().convert("RGB")
        page_text = pytesseract.image_to_string(image, lang="eng")
        if page_text and page_text.strip():
            extracted_pages.append(page_text.strip())

    return "\n".join(extracted_pages).strip()


def _read_uploaded_file_bytes(uploaded_file):
    """Read uploaded file bytes safely for repeated parsing attempts."""
    try:
        if hasattr(uploaded_file, "getvalue"):
            data = uploaded_file.getvalue()
            if data:
                return data

        if hasattr(uploaded_file, "seek"):
            uploaded_file.seek(0)
        data = uploaded_file.read()
        if hasattr(uploaded_file, "seek"):
            uploaded_file.seek(0)
        return data
    except Exception:
        return b""


def _ocr_is_available():
    """Return True when OCR dependencies and the Tesseract executable are installed."""
    return (
        importlib.util.find_spec("pytesseract") is not None
        and importlib.util.find_spec("pypdfium2") is not None
        and _find_tesseract_path() is not None
    )


def _find_tesseract_path():
    """Find the Tesseract executable from PATH or common Windows install locations."""
    path_from_env = shutil.which("tesseract")
    if path_from_env:
        return path_from_env

    common_paths = [
        "/usr/bin/tesseract",
        "/usr/local/bin/tesseract",
        os.path.join(
            os.environ.get("LOCALAPPDATA", ""),
            "Programs",
            "Tesseract-OCR",
            "tesseract.exe",
        ),
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    ]

    for candidate_path in common_paths:
        if candidate_path and os.path.exists(candidate_path):
            return candidate_path

    return None
