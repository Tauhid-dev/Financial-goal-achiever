"""
Pure pipeline orchestrator – code‑only, no side effects.

The function stitches together the existing pure‑function modules:
- PDF ingestion (extract_text_from_pdf)
- Privacy redaction & sanitisation
- Dynamic parser selection (registry)
- Normalisation
- Budget aggregation & health analysis
- Optional goal projection / simulation (if a goal dict is supplied)

All operations are pure and return data structures; no DB writes,
no external calls, and no exceptions are raised for unknown inputs.
"""

from typing import Dict, List, Optional

# Ingest
from backend.app.modules.ingest.pdf_reader import extract_text_from_pdf
from backend.app.modules.ingest import registry

# Privacy
from backend.app.modules.privacy.redactor import redact_text
from backend.app.modules.privacy.sanitizer import sanitize_transactions

# Normalisation
from backend.app.modules.normalize.normalizer import normalize_transactions

# Budget
from backend.app.modules.budget.aggregator import aggregate_by_month
from backend.app.modules.budget.analyzer import analyze_budget

# Goals (optional – placeholder calls if implementations exist)
try:
    from backend.app.modules.goals.projection import project_time_to_goal
    from backend.app.modules.goals.simulator import simulate_goal
except Exception:
    # Goal functions may not be implemented yet; we will skip them safely.
    project_time_to_goal = None  # type: ignore
    simulate_goal = None  # type: ignore


def _latest_month_summary(monthly_summary: Dict) -> Optional[Dict]:
    """
    Return the summary dict for the most recent month.
    If the dict is empty, return None.
    """
    if not monthly_summary:
        return None
    # Assuming keys are sortable month strings like "2023-07"
    latest_key = max(monthly_summary.keys())
    return monthly_summary[latest_key]


def process_pdf(
    file_path: str,
    family_id: Optional[str] = None,
    goal: Optional[Dict] = None,
) -> Dict:
    """
    Orchestrates the full PDF processing pipeline.

    Parameters
    ----------
    file_path: str
        Path to the PDF file on the local filesystem.
    family_id: str | None
        Identifier of the family the document belongs to (currently unused,
        kept for future DB wiring).
    goal: dict | None
        Optional goal definition – if supplied, the pipeline will attempt to
        run a projection or simulation using the goal module (if available).

    Returns
    -------
    dict
        {
            "redactions": List[str],
            "transactions_normalized": List[Dict],
            "monthly_summary": Dict,
            "budget_health": Dict,
            "goal": Dict (optional)
        }
    """
    # 1. Extract raw text from PDF (pure stub – returns empty string on failure)
    # Ensure the temporary file is removed after processing (handled by caller)
    raw_text = extract_text_from_pdf(file_path)

    # 2. Redact sensitive data
    redacted_text, redactions = redact_text(raw_text)

    # 3. Choose a parser based on the (redacted) text
    parser = registry.get_parser_for_text(redacted_text)

    # 4. Extract raw transaction dicts (fallback to empty list)
    raw_transactions: List[Dict] = parser.extract(redacted_text) if parser else []

    # 5. Sanitize transactions (remove/ mask sensitive fields)
    safe_transactions = sanitize_transactions(raw_transactions)

    # 6. Normalise to deterministic transaction objects
    normalized_transactions = normalize_transactions(safe_transactions)

    # 7. Aggregate by month
    monthly_summary = aggregate_by_month(normalized_transactions)

    # 8. Analyse budget health – use the latest month if available
    latest_summary = _latest_month_summary(monthly_summary)
    budget_health = analyze_budget(latest_summary) if latest_summary else {}

    # 9. Optional goal handling
    goal_result: Dict = {}
    if goal:
        if project_time_to_goal:
            try:
                goal_result["projection"] = project_time_to_goal(goal, normalized_transactions)
            except Exception:
                goal_result["projection"] = {}
        if simulate_goal:
            try:
                goal_result["simulation"] = simulate_goal(goal, normalized_transactions)
            except Exception:
                goal_result["simulation"] = {}

    # Assemble final payload
    return {
        "redactions": redactions,
        "transactions_normalized": [t.dict() if hasattr(t, "dict") else t for t in normalized_transactions],
        "monthly_summary": monthly_summary,
        "budget_health": budget_health,
        **({"goal": goal_result} if goal_result else {}),
    }
