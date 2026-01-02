import pytest
from backend.app.main import app
from backend.app.auth.deps import get_current_user
from backend.app.db.session import get_async_session

class DummyUser:
    id = "u1"
    email = "test@example.com"

async def override_get_current_user():
    return DummyUser()

async def override_get_async_session():
    # Return None; endpoints that need a session will not be called in these tests
    return None

@pytest.fixture(autouse=True)
def apply_overrides():
    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[get_async_session] = override_get_async_session
    yield
    app.dependency_overrides.clear()
