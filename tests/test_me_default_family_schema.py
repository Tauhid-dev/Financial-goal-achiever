import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
# Removed direct import of get_current_user; will be monkeypatched on the route level
from backend.app.db.repositories.membership_repo import get_default_family_id_for_user

# Dummy user for auth override
class DummyUser:
    id: str = "u1"
    email: str = "test@example.com"

client = TestClient(app)

@pytest.fixture(autouse=True)
def override_deps(monkeypatch):
    # Override auth dependency to bypass JWT check
    monkeypatch.setattr(
        "backend.app.auth.deps.get_current_user",
        lambda: DummyUser()
    )
    # Also override the imported reference used in the route
    monkeypatch.setattr(
        "backend.app.api.routes.get_current_user",
        lambda: DummyUser()
    )
    monkeypatch.setattr(
        "backend.app.api.routes.get_current_user",
        lambda: DummyUser()
    )
    # Override family lookup
    monkeypatch.setattr(
        "backend.app.db.repositories.membership_repo.get_default_family_id_for_user",
        lambda session, user_id: "f1",
    )
    # Override async DB session to avoid aiosqlite requirement
    monkeypatch.setattr(
        "backend.app.db.session.get_async_session",
        lambda: None,
    )
    yield
    # Cleanup is automatic

def test_default_family_endpoint():
    response = client.get("/api/me/default-family")
    assert response.status_code == 200
    assert response.json() == {"family_id": "f1"}
