import pytest
# Import the projection and simulation functions directly from their modules
from backend.app.modules.goals.projection import project_time_to_goal
from backend.app.modules.goals.simulator import simulate

def test_project_time_to_goal():
    goal = {"target_amount": 10000, "monthly_contribution": 500}
    # Provide a minimal list of normalized transactions (empty is fine for this stub)
    transactions = []
    result = project_time_to_goal(goal, transactions)
    assert isinstance(result, dict)
    assert "months_required" in result

def test_simulate():
    goal = {"target_amount": 10000, "monthly_contribution": 500}
    transactions = []
    result = simulate(goal, transactions)
    assert isinstance(result, dict)
    assert "months_required" in result
