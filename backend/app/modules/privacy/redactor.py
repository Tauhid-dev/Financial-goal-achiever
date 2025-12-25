import re
from .patterns import SENSITIVE_PATTERNS

def redact_text(text: str) -> tuple[str, list[str]]:
    """
    Scan the input text for known sensitive patterns and replace them with
    placeholder tokens. Returns a tuple of (redacted_text, list_of_applied_types).

    Example token: [REDACTED_ACCOUNT], [REDACTED_CARD], etc.
    """
    applied = []
    redacted = text

    for name, pattern in SENSITIVE_PATTERNS.items():
        # Compile with case‑insensitive flag where appropriate
        flags = re.IGNORECASE if name == "email" else 0
        regex = re.compile(pattern, flags)

        if regex.search(redacted):
            token = f"[REDACTED_{name.upper()}]"
            redacted = regex.sub(token, redacted)
            applied.append(name)

    return redacted, applied
