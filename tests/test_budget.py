import pytest
from backend.app.modules.budget.aggregator import aggregate_by_month
from backend.app.modules.budget.analyzer import analyze_budget

def test_aggregate_by_month():
    transactions = [
        {"date": "2023-01-15", "amount": 1000, "direction": "income"},
        {"date": "2023-01-20", "amount": -200, "direction": "expense"},
        {"date": "2023-02-05", "amount": 1500, "direction": "income"},
    ]
    summary = aggregate_by_month(transactions)
    assert "2023-01" in summary
    assert "2023-02" in summary
    assert summary["2023-01"]["income"] == 1000
    assert summary["2023-01"]["expenses"] == 200

def test_analyze_budget():
    month_summary = {"income": 3000, "expenses": 1500, "savings_rate": 0.5}
    result = analyze_budget(month_summary)
    assert result["status"] in ("healthy", "warning", "critical")
    # Ensure the result contains a numeric health score
    assert isinstance(result["health_score"], float)
