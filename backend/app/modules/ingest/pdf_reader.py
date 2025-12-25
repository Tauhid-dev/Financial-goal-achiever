import pdfplumber

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract raw text from a PDF file using pdfplumber.
    Returns an empty string if no text can be extracted.
    """
    try:
        with pdfplumber.open(file_path) as pdf:
            pages_text = [page.extract_text() or "" for page in pdf.pages]
        return "\n".join(pages_text).strip()
    except Exception:
        # Any error (file not found, corrupted PDF, etc.) results in empty string
        return ""
