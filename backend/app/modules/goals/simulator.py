from .schema import SavingsGoal
from .projection import project_time_to_goal

def simulate(
    goal: SavingsGoal,
    extra_monthly_savings: float = 0.0,
    extra_monthly_income: float = 0.0,
    reduced_monthly_expenses: float = 0.0,
) -> dict:
    """
    Perform a what‑if simulation by adjusting the effective monthly contribution.
    The original `goal` instance is never mutated.
    Effective contribution = base contribution + extra_savings + extra_income - reduced_expenses
    Returns the same dict structure as `project_time_to_goal`.
    """
    effective_contribution = (
        goal.monthly_contribution
        + extra_monthly_savings
        + extra_monthly_income
        - reduced_monthly_expenses
    )

    # Build a temporary goal with the adjusted contribution
    temp_goal = SavingsGoal(
        id=goal.id,
        name=goal.name,
        target_amount=goal.target_amount,
        current_amount=goal.current_amount,
        monthly_contribution=effective_contribution,
        target_date=goal.target_date,
    )
    return project_time_to_goal(temp_goal)
