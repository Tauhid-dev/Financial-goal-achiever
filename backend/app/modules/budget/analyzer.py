from typing import Dict

def analyze_budget(monthly_summary: Dict) -> Dict:
    """
    Derive simple health metrics from a single month summary.
    Expected input shape matches the output of `aggregate_by_month`.
    Returns a dict with:
        - savings_rate: float (savings / income)
        - largest_category: str
        - expense_ratio: float (expenses / income)
        - status: "healthy" | "warning" | "risky"
    """
    income = monthly_summary.get("income", 0.0)
    expenses = monthly_summary.get("expenses", 0.0)

    if income == 0:
        # Avoid division by zero – treat as risky
        return {
            "savings_rate": 0.0,
            "largest_category": None,
            "expense_ratio": 0.0,
            "status": "risky",
        }

    savings = income - expenses
    savings_rate = round(savings / income, 3)
    expense_ratio = round(expenses / income, 3)

    # Determine the category with the highest spend
    categories = monthly_summary.get("categories", {})
    largest_category = max(categories, key=categories.get) if categories else None

    # Simple status rules
    if savings_rate >= 0.30:
        status = "healthy"
    elif 0.10 <= savings_rate < 0.30:
        status = "warning"
    else:
        status = "risky"

    return {
        "savings_rate": savings_rate,
        "largest_category": largest_category,
        "expense_ratio": expense_ratio,
        "status": status,
    }
