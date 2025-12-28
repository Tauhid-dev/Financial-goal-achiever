import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from backend.app.modules.models.orm import Base  # ensures models are registered

# Default database URL; can be overridden via environment variable
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@postgres:5432/financial_db",
)

# Async engine
# Lazy engine creation to avoid side‑effects at import time
def get_engine():
    return create_async_engine(DATABASE_URL, echo=False, future=True)

# Async session factory using lazy engine
def get_async_sessionmaker():
    return async_sessionmaker(
        bind=get_engine(),
        class_=AsyncSession,
        expire_on_commit=False,
    )

# Dependency helper for FastAPI routes
async def get_session() -> AsyncSession:
    async_session = get_async_sessionmaker()
    async with async_session() as session:
        yield session
