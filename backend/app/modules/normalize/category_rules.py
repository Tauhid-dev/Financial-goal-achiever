from typing import Tuple

# Simple keyword‑to‑category mapping (all lower‑case)
CATEGORY_RULES = {
    "Food": ["grocery", "restaurant", "cafe", "uber eats", "supermarket"],
    "Transport": ["uber", "taxi", "bus", "train", "metro", "fuel"],
    "Housing": ["rent", "mortgage", "lease"],
    "Utilities": ["electric", "gas", "water", "internet", "phone"],
    "Entertainment": ["cinema", "movie", "concert", "netflix", "spotify"],
    "Healthcare": ["pharmacy", "hospital", "clinic", "dentist"],
}

def categorize(description: str) -> Tuple[str, float]:
    """
    Return a (category, confidence) pair based on keyword matching.
    - Matching is case‑insensitive.
    - First matching keyword wins.
    - If no keyword matches, category = "Other" and confidence = 0.3.
    """
    lowered = description.lower()
    for category, keywords in CATEGORY_RULES.items():
        for kw in keywords:
            if kw in lowered:
                # Confidence is modest for simple keyword match
                return category, 0.6
    return "Other", 0.3
