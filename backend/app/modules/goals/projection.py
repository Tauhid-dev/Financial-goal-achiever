from math import ceil
from backend.app.modules.goals.schema import SavingsGoal
from backend.app.modules.models.schemas import GoalProjectionSchema

def project_time_to_goal(goal: SavingsGoal) -> dict:
    """
    Estimate how long it will take to reach the goal.
    - If monthly_contribution <= 0 the goal is not achievable.
    - No interest or inflation is considered (v1 simplicity).
    Returns:
        {
            "months_required": int,
            "years_required": float,
            "is_achievable": bool
        }
    """
    remaining = max(goal.target_amount - goal.current_amount, 0.0)

    if goal.monthly_contribution <= 0:
        return {
            "months_required": 0,
            "years_required": 0.0,
            "is_achievable": False,
        }

    months = ceil(remaining / goal.monthly_contribution)
    years = round(months / 12, 2)

    return {
        "months_required": months,
        "years_required": years,
        "is_achievable": True,
    }
