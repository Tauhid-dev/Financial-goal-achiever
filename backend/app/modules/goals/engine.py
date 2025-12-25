from .schemas import GoalInput, GoalResult

class GoalEngine:
    """
    Pure‑math engine that evaluates whether a financial goal is achievable.
    No advice or probabilistic statements – only straightforward arithmetic.
    """

    @staticmethod
    def evaluate(goal: GoalInput) -> GoalResult:
        # Required savings each month to hit the target within the horizon
        required_per_month = goal.target_amount / goal.time_horizon_months

        # Difference between what is available and what is required
        diff = goal.monthly_surplus - required_per_month

        # Feasibility flag – true if surplus covers the required amount
        feasible = diff >= 0

        return GoalResult(
            required_savings_per_month=round(required_per_month, 2),
            shortfall_or_surplus=round(diff, 2),
            feasible=feasible,
        )
