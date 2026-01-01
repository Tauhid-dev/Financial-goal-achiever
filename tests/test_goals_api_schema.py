import pytest
from dataclasses import dataclass
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.auth.deps import get_current_user

@dataclass
class DummyUser:
    id: str
    email: str

client = TestClient(app)

def test_create_goal_schema_enforcement():
    # Override auth dependency to bypass 401 and reach schema validation
    app.dependency_overrides[get_current_user] = lambda: DummyUser(id="u1", email="test@example.com")

    # Payload missing required field 'target_amount' should trigger 422 validation error.
    payload = {
        "name": "New Goal",
        # "target_amount" omitted intentionally
        "current_amount": 0.0,
        "monthly_contribution": 100.0,
        "target_date": None,
    }
    response = client.post("/api/goals", json=payload)
    # Assert strict 422 for schema validation
    assert response.status_code == 422
    assert "target_amount" in response.text

    # Clean up override
    app.dependency_overrides = {}
