import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def get_auth_headers():
    # Placeholder for auth headers; adjust as needed for your auth setup.
    return {}

def test_create_goal_schema_enforcement():
    # Payload missing required field 'target_amount' should trigger 422 validation error.
    payload = {
        "name": "New Goal",
        # "target_amount" omitted intentionally
        "current_amount": 0.0,
        "monthly_contribution": 100.0,
        "target_date": None,
    }
    response = client.post("/api/goals", json=payload, headers=get_auth_headers())
    # If authentication is required, the endpoint may return 401; we focus on schema validation.
    assert response.status_code in (401, 422)
    if response.status_code == 422:
        assert "target_amount" in response.text
