from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.auth.deps import get_current_user
from backend.app.db.session import get_async_session
from backend.app.db.models.user import User
from backend.app.modules.models.scope import ScopeDTO
from backend.app.db.repositories.scope_repo import list_scopes_for_user, get_default_scope_for_user

router = APIRouter(prefix="/api/scopes", tags=["Scopes"])

@router.get("", response_model=List[ScopeDTO])
async def list_scopes(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
) -> List[ScopeDTO]:
    """
    List all scopes (families) the authenticated user belongs to.
    """
    return await list_scopes_for_user(session, current_user.id)

@router.get("/default", response_model=ScopeDTO)
async def get_default_scope(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
) -> ScopeDTO:
    """
    Return the default scope for the user.
    """
    scope = await get_default_scope_for_user(session, current_user.id)
    if not scope:
        raise HTTPException(status_code=404, detail="No default scope found")
    return scope
