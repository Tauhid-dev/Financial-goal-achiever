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
from dataclasses import asdict

# Goals (optional – placeholder calls if implementations exist)
try:
    from backend.app.modules.goals.projection import project_time_to_goal
    from backend.app.modules.goals.simulator import simulate
    from backend.app.modules.goals.schema import SavingsGoal
except Exception:
    project_time_to_goal = None  # type: ignore
    simulate = None  # type: ignore
    SavingsGoal = None  # type: ignore


def _latest_month_summary(monthly_summary: Dict) -> Optional[Dict]:
    """
    Return the summary dict for the most recent month.
    If the dict is empty, return None.
    """
    if not monthly_summary:
        return None
    latest_key = max(monthly_summary.keys())
    return monthly_summary[latest_key]


def _goal_from_dict(goal: dict) -> Optional[SavingsGoal]:
    """
    Convert a raw goal dict into a SavingsGoal dataclass.
    Missing fields get safe defaults. Returns None on any error.
    """
    if SavingsGoal is None:
        return None
    try:
        return SavingsGoal(
            id=goal.get("id", ""),
            name=goal.get("name", ""),
            target_amount=float(goal.get("target_amount", 0)),
            current_amount=float(goal.get("current_amount", 0)),
            monthly_contribution=float(goal.get("monthly_contribution", 0)),
            target_date=goal.get("target_date"),
        )
    except Exception:
        return None


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
    raw_text = extract_text_from_pdf(file_path)
    redacted_text, redactions = redact_text(raw_text)
    parser = registry.get_parser_for_text(redacted_text)
    raw_transactions: List[Dict] = parser.extract(redacted_text) if parser else []
    safe_transactions = sanitize_transactions(raw_transactions)
    normalized_transactions = normalize_transactions(safe_transactions)
    monthly_summary = aggregate_by_month(normalized_transactions)
    latest_summary = _latest_month_summary(monthly_summary)
    budget_health = analyze_budget(latest_summary) if latest_summary else {}

    goal_result: Dict = {}
    if goal and _goal_from_dict(goal):
        goal_obj = _goal_from_dict(goal)
        if project_time_to_goal:
            try:
                goal_result["projection"] = project_time_to_goal(goal_obj)
            except Exception:
                goal_result["projection"] = {}
        if simulate:
            try:
                goal_result["simulation"] = simulate(goal_obj)
            except Exception:
                goal_result["simulation"] = {}

    return {
        "redactions": redactions,
        "transactions_normalized": [asdict(t) for t in normalized_transactions],
        "monthly_summary": monthly_summary,
        "budget_health": budget_health,
        **({"goal": goal_result} if goal_result else {}),
    }
