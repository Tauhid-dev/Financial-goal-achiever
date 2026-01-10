from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .config import DBConfig

_engine = None
_sessionmaker = None

def get_async_engine():
    """
    Lazy creation of the async engine. The engine is instantiated only when
    a session is requested, never at import time.
    """
    global _engine
    if _engine is None:
        cfg = DBConfig()
        _engine = create_async_engine(cfg.DATABASE_URL, echo=False, future=True)
    return _engine

def get_async_sessionmaker():
    """
    Lazy creation of the async sessionmaker. It is instantiated only when
    a session is first needed.
    """
    global _sessionmaker
    if _sessionmaker is None:
        _sessionmaker = sessionmaker(
            bind=get_async_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return _sessionmaker

async def get_async_session() -> AsyncSession:
    """
    FastAPI dependency (or generic async context) that yields an async session.
    The session is closed automatically when the generator exits.
    """
    SessionLocal = get_async_sessionmaker()
    async with SessionLocal() as session:
        yield session
