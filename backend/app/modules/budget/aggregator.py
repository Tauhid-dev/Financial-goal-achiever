from collections import defaultdict
from typing import List, Dict
from ..normalize.schema import NormalizedTransaction

def aggregate_by_month(
    transactions: List[NormalizedTransaction],
) -> Dict[str, Dict]:
    """
    Produce a month‑level aggregation.
    Output example:
    {
        "2024-01": {
            "income": 5000.0,
            "expenses": 3200.0,
            "categories": {
                "Food": 800.0,
                "Transport": 300.0,
                ...
            }
        },
        ...
    }
    """
    monthly: Dict[str, Dict] = defaultdict(
        lambda: {"income": 0.0, "expenses": 0.0, "categories": defaultdict(float)}
    )

    for txn in transactions:
        # Guard against malformed dates – skip if we cannot extract YYYY‑MM
        try:
            month_key = txn.date[:7]  # expects "YYYY-MM-DD" or similar
        except Exception:
            continue

        if txn.direction == "income":
            monthly[month_key]["income"] += txn.amount
        else:
            monthly[month_key]["expenses"] += abs(txn.amount)

        # Category aggregation (use the category already assigned by normalizer)
        monthly[month_key]["categories"][txn.category] += abs(txn.amount)

    # Convert inner defaultdicts to plain dicts for a clean JSON‑serialisable shape
    result: Dict[str, Dict] = {}
    for month, data in monthly.items():
        result[month] = {
            "income": data["income"],
            "expenses": data["expenses"],
            "categories": dict(data["categories"]),
        }
    return result
