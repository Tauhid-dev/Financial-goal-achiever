import pytest
from backend.app.modules.goals.schema import SavingsGoal
from backend.app.modules.goals.projection import project_time_to_goal
from backend.app.modules.goals.simulator import simulate

def test_project_time_to_goal():
    goal = SavingsGoal(
        id="g1",
        name="Test Goal",
        target_amount=10000,
        current_amount=0,
        monthly_contribution=500,
        target_date=None,
    )
    result = project_time_to_goal(goal)
    assert isinstance(result, dict)
    assert isinstance(result.get("months_required"), int)
    assert isinstance(result.get("years_required"), float)
    assert isinstance(result.get("is_achievable"), bool)

def test_simulate():
    goal = SavingsGoal(
        id="g1",
        name="Test Goal",
        target_amount=10000,
        current_amount=0,
        monthly_contribution=500,
        target_date=None,
    )
    result = simulate(
        goal,
        extra_monthly_savings=100,
        extra_monthly_income=0,
        reduced_monthly_expenses=0,
    )
    assert isinstance(result, dict)
    assert isinstance(result.get("months_required"), int)
    assert isinstance(result.get("years_required"), float)
    assert isinstance(result.get("is_achievable"), bool)
