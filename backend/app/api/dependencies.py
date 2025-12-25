from fastapi import Depends
from ..core.database import get_session

# Dependency that yields an async DB session for services that need it
async def db_session():
    async for session in get_session():
        yield session
