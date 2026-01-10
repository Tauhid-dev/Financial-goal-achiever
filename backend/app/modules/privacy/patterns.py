# Regular expression patterns for common sensitive data types.
# These are simple patterns for demonstration; real‑world use would require stricter validation.
SENSITIVE_PATTERNS = {
    # Bank account numbers – 8‑12 digits (generic)
    "account_number": r"\b\d{8,12}\b",
    # Credit / debit card numbers – 13‑19 digits, optional spaces or dashes
    "card_number": r"\b(?:\d[ -]*?){13,19}\b",
    # BSB / routing numbers – 6 digits (Australia)
    "bsb": r"\b\d{6}\b",
    # IBAN‑like numbers – starts with 2 letters followed by 10‑30 alphanumerics
    "iban": r"\b[A-Z]{2}[0-9A-Z]{10,30}\b",
    # Email addresses – simple pattern
    "email": r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
}
