import pytest
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from backend.app.db.base import Base

# Enable pytest-asyncio plugin for async fixtures
pytest_plugins = ["pytest_asyncio"]

# -----------------------------------------------------------------
# Environment setup – must happen before importing the FastAPI app
# -----------------------------------------------------------------
os.environ.setdefault("JWT_SECRET", "test-secret")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

# -----------------------------------------------------------------
# Import after env vars are set so Config reads the test values
# -----------------------------------------------------------------
from backend.app.main import app
from backend.app.auth.deps import get_current_user
from backend.app.db.session import get_async_session

# -----------------------------------------------------------------
# Async engine fixture (session‑wide)
# -----------------------------------------------------------------
import pytest_asyncio

# -----------------------------------------------------------------
# Async engine fixture (session‑wide)
# -----------------------------------------------------------------
@pytest.fixture(scope="session")
def async_engine():
    return create_async_engine(os.getenv("DATABASE_URL"), future=True, echo=False)

# -----------------------------------------------------------------
# Create / drop tables once per test session
# -----------------------------------------------------------------
@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database(async_engine):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

# -----------------------------------------------------------------
# Provide a real AsyncSession for each test
# -----------------------------------------------------------------
@pytest_asyncio.fixture
async def db_session(async_engine):
    async_session = async_sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

# -----------------------------------------------------------------
# Dummy user for auth override
# -----------------------------------------------------------------
class DummyUser:
    id = "u1"
    email = "test@example.com"

async def override_get_current_user():
    return DummyUser()

# -----------------------------------------------------------------
# Apply overrides automatically for every test
# -----------------------------------------------------------------
@pytest.fixture(autouse=True)
def apply_overrides(db_session):
    app.dependency_overrides[get_current_user] = override_get_current_user
    # FastAPI will await this coroutine and receive the session object
    app.dependency_overrides[get_async_session] = lambda: db_session
    yield
    app.dependency_overrides.clear()
