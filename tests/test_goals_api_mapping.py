import types

import pytest
from backend.app.modules.models.schemas import GoalWithProjectionSchema, GoalProjectionSchema
from backend.app.modules.goals.schema import SavingsGoal
from backend.app.modules.goals.projection import project_time_to_goal

@pytest.fixture
def fake_db_goal():
    # Simple object mimicking the DB model
    goal = types.SimpleNamespace(
        id="goal-123",
        family_id="family-abc",
        name="Vacation",
        target_amount=5000.0,
        current_amount=1500.0,
        monthly_contribution=200.0,
        target_date="2025-12-31",
    )
    return goal

def test_projection_mapping(fake_db_goal):
    # Convert DB goal to SavingsGoal
    savings_goal = SavingsGoal(
        id=fake_db_goal.id,
        family_id=fake_db_goal.family_id,
        name=fake_db_goal.name,
        target_amount=fake_db_goal.target_amount,
        current_amount=fake_db_goal.current_amount,
        monthly_contribution=fake_db_goal.monthly_contribution,
        target_date=fake_db_goal.target_date,
    )
    # Compute projection
    projection = project_time_to_goal(savings_goal)
    # Ensure projection has expected fields and types
    if isinstance(projection, dict):
        projection = GoalProjectionSchema(**projection)
    assert isinstance(projection, GoalProjectionSchema)
    assert isinstance(projection.months_required, int)
    assert isinstance(projection.years_required, float)
    assert isinstance(projection.is_achievable, bool)

    # Build final schema
    result = GoalWithProjectionSchema(
        id=fake_db_goal.id,
        family_id=fake_db_goal.family_id,
        name=fake_db_goal.name,
        target_amount=fake_db_goal.target_amount,
        current_amount=fake_db_goal.current_amount,
        monthly_contribution=fake_db_goal.monthly_contribution,
        target_date=fake_db_goal.target_date,
        projection=projection,
    )
    # Verify fields are correctly set
    assert result.id == fake_db_goal.id
    assert result.projection == projection
