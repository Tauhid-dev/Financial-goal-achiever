import re
from .patterns import SENSITIVE_PATTERNS

def assert_safe_for_processing(data: str) -> bool:
    """
    Quick check that the supplied string does NOT contain any unredacted
    sensitive patterns. Returns True if safe, False otherwise.
    No exceptions are raised – callers can decide how to handle a False result.
    """
    for pattern in SENSITIVE_PATTERNS.values():
        if re.search(pattern, data):
            return False
    return True
