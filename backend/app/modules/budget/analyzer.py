from typing import Dict

def analyze_budget(monthly_summary: Dict) -> Dict:
    """
    Derive simple health metrics from a single month summary.
    Expected input shape matches the output of `aggregate_by_month`.
    Returns a dict with:
        - savings_rate: float (savings / income)
        - largest_category: str | None
        - expense_ratio: float (expenses / income)
        - status: "healthy" | "warning" | "risky"
        - health_score: float
    """
    income = float(monthly_summary.get("income", 0))
    expenses = float(monthly_summary.get("expenses", 0))

    # Compute savings and rates safely
    if income > 0:
        savings = max(income - expenses, 0)
        savings_rate = savings / income
        expense_ratio = expenses / income
    else:
        savings_rate = 0.0
        expense_ratio = 0.0

    # Determine status using the same thresholds
    if savings_rate >= 0.30:
        status = "healthy"
    elif savings_rate >= 0.10:
        status = "warning"
    else:
        status = "risky"

    # Largest category (may be missing)
    categories = monthly_summary.get("categories", {})
    largest_category = max(categories, key=categories.get) if categories else None

    # Health score – always present
    health_score = round(max(0.0, min(100.0, savings_rate * 100.0)), 2)

    return {
        "savings_rate": savings_rate,
        "largest_category": largest_category,
        "expense_ratio": expense_ratio,
        "status": status,
        "health_score": health_score,
    }
