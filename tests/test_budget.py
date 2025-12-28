import pytest
from backend.app.modules.normalize.schema import NormalizedTransaction
from backend.app.modules.budget.aggregator import aggregate_by_month
from backend.app.modules.budget.analyzer import analyze_budget

def test_aggregate_and_analyze():
    txns = [
        NormalizedTransaction(
            id="t1",
            date="2023-01-15",
            description="Salary",
            amount=1000.0,
            direction="income",
            category="Salary",
            subcategory=None,
            confidence=1.0,
        ),
        NormalizedTransaction(
            id="t2",
            date="2023-01-20",
            description="Groceries",
            amount=-200.0,
            direction="expense",
            category="Food",
            subcategory=None,
            confidence=1.0,
        ),
        NormalizedTransaction(
            id="t3",
            date="2023-02-05",
            description="Freelance",
            amount=1500.0,
            direction="income",
            category="Side Income",
            subcategory=None,
            confidence=1.0,
        ),
    ]

    monthly = aggregate_by_month(txns)
    assert "2023-01" in monthly
    assert "2023-02" in monthly
    assert monthly["2023-01"]["income"] == 1000.0
    assert monthly["2023-01"]["expenses"] == 200.0

    analysis = analyze_budget(monthly["2023-01"])
    assert isinstance(analysis["savings_rate"], float)
    assert isinstance(analysis["largest_category"], (str, type(None)))
    assert isinstance(analysis["expense_ratio"], float)
    assert isinstance(analysis["health_score"], float)
    assert analysis["status"] in ("healthy", "warning", "risky", "critical")
