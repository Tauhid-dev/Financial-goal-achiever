from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .config import DBConfig

def get_async_engine():
    """
    Lazy creation of the async engine. The engine is instantiated only when
    a session is requested, never at import time.
    """
    cfg = DBConfig()
    return create_async_engine(cfg.DATABASE_URL, echo=False, future=True)

# Async session factory
AsyncSessionLocal = sessionmaker(
    bind=get_async_engine(),
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_async_session() -> AsyncSession:
    """
    FastAPI dependency (or generic async context) that yields an async session.
    The session is closed automatically when the generator exits.
    """
    async with AsyncSessionLocal() as session:
        yield session
