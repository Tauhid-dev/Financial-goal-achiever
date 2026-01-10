from .schema import SavingsGoal
from .projection import project_time_to_goal
from .simulator import simulate
from .recommendations import recommend_adjustments

__all__ = [
    "SavingsGoal",
    "project_time_to_goal",
    "simulate",
    "recommend_adjustments",
]
