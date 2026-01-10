"""
Pure‑function mapping utilities for the Goals API.

These functions are deliberately free of FastAPI, DB session, or any side‑effects.
They take a DB row (or any object with the same attributes) and return plain
dictionaries that match the Pydantic schemas used by the API.
"""

from __future__ import annotations

from backend.app.modules.goals.schema import SavingsGoal
from backend.app.modules.models.schemas import GoalProjectionSchema, GoalWithProjectionSchema
from backend.app.modules.goals.projection import project_time_to_goal


def goal_row_to_schema(goal_row) -> dict:
    """
    Map a DB Goal row (or any object with the required attributes)
    to the plain dict shape of GoalSchema.
    """
    return {
        "id": goal_row.id,
        "family_id": goal_row.family_id,
        "name": goal_row.name,
        "target_amount": goal_row.target_amount,
        "current_amount": goal_row.current_amount,
        "monthly_contribution": goal_row.monthly_contribution,
        "target_date": goal_row.target_date,
    }


def goal_row_to_with_projection(goal_row) -> dict:
    """
    Build a SavingsGoal dataclass from the DB row, run the projection
    logic and return a dict matching GoalWithProjectionSchema.
    """
    # Build the dataclass expected by the projection function
    savings = SavingsGoal(
        id=goal_row.id,
        family_id=goal_row.family_id,
        name=goal_row.name,
        target_amount=goal_row.target_amount,
        current_amount=goal_row.current_amount,
        monthly_contribution=goal_row.monthly_contribution,
        target_date=goal_row.target_date,
    )

    # Deterministic projection (returns a plain dict)
    projection_dict = project_time_to_goal(savings)

    # Assemble the final shape
    return {
        "id": goal_row.id,
        "family_id": goal_row.family_id,
        "name": goal_row.name,
        "target_amount": goal_row.target_amount,
        "current_amount": goal_row.current_amount,
        "monthly_contribution": goal_row.monthly_contribution,
        "target_date": goal_row.target_date,
        "projection": projection_dict,
    }
