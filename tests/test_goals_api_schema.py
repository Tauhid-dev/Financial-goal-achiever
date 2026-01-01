import pytest
from dataclasses import dataclass
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.auth.deps import get_current_user

# ----------------------------------------------------------------------
# Dummy user for auth overrides
# ----------------------------------------------------------------------
@dataclass
class DummyUser:
    id: str
    email: str

client = TestClient(app)

# ----------------------------------------------------------------------
# Global fixture to override dependencies for all tests in this file
# ----------------------------------------------------------------------
@pytest.fixture(autouse=True)
def override_dependencies(monkeypatch):
    # Override auth to always return dummy user
    app.dependency_overrides[get_current_user] = lambda: DummyUser(id="test-user", email="test@example.com")

    # Mock authz check to be a no‑op
    async def fake_assert_family_access(session, user_id, family_id):
        return True

    monkeypatch.setattr("backend.app.api.routes.assert_family_access", fake_assert_family_access)

    # Mock repository functions used by the goals endpoints
    async def fake_create_goal(session, family_id, name, target_amount, current_amount=0.0,
                               monthly_contribution=0.0, target_date=None):
        class Obj:
            id = "goal-id"
            family_id = family_id
            name = name
            target_amount = target_amount
            current_amount = current_amount
            monthly_contribution = monthly_contribution
            target_date = target_date
        return Obj()

    async def fake_list_goals(session, family_id):
        return [await fake_create_goal(session, family_id, "Goal 1", 100.0)]

    async def fake_delete_goal(session, family_id, goal_id):
        return True

    monkeypatch.setattr("backend.app.api.routes.repo_create_goal", fake_create_goal)
    monkeypatch.setattr("backend.app.api.routes.repo_list_goals", fake_list_goals)
    monkeypatch.setattr("backend.app.api.routes.repo_delete_goal", fake_delete_goal)

    # Mock projection helper to return a plain dict
    def fake_projection(goal_obj):
        return {
            "id": goal_obj.id,
            "family_id": goal_obj.family_id,
            "name": goal_obj.name,
            "target_amount": goal_obj.target_amount,
            "current_amount": goal_obj.current_amount,
            "monthly_contribution": goal_obj.monthly_contribution,
            "target_date": goal_obj.target_date,
            "projection": None,
        }

    monkeypatch.setattr("backend.app.api.routes.goal_row_to_with_projection", fake_projection)

    yield
    # Cleanup overrides after each test
    app.dependency_overrides = {}
    monkeypatch.undo()


def test_create_goal_schema_enforcement():
    # Missing required field 'target_amount' should trigger 422 validation error.
    payload = {
        "name": "New Goal",
        "current_amount": 0.0,
        "monthly_contribution": 100.0,
        "target_date": None,
    }
    response = client.post("/api/goals/family-123", json=payload)
    assert response.status_code == 422
    assert "target_amount" in response.text


def test_create_goal_success():
    payload = {
        "name": "New Goal",
        "target_amount": 200.0,
        "current_amount": 0.0,
        "monthly_contribution": 50.0,
        "target_date": None,
    }
    response = client.post("/api/goals/family-123", json=payload)
    assert response.status_code == 200
    data = response.json()
    expected_keys = {
        "id",
        "family_id",
        "name",
        "target_amount",
        "current_amount",
        "monthly_contribution",
        "target_date",
        "projection",
    }
    assert expected_keys.issubset(data.keys())
    assert data["family_id"] == "family-123"


def test_list_goals():
    response = client.get("/api/goals/family-123")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    goal = data[0]
    expected_keys = {
        "id",
        "family_id",
        "name",
        "target_amount",
        "current_amount",
        "monthly_contribution",
        "target_date",
        "projection",
    }
    assert expected_keys.issubset(goal.keys())
    assert goal["family_id"] == "family-123"


def test_delete_goal():
    response = client.delete("/api/goals/family-123/goal-id")
    assert response.status_code == 200
    assert response.json() == {"deleted": True}
