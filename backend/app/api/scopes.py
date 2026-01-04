from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.auth.deps import get_current_user
from backend.app.db.session import get_async_session
from backend.app.db.models import User
from backend.app.db.repositories import membership_repo
from backend.app.modules.models.schemas import ScopeSchema

router = APIRouter(prefix="/api/scopes", tags=["Scopes"])

@router.get("/default", response_model=ScopeSchema)
async def get_default_scope(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """
    Return the default scope for the authenticated user.
    Currently only supports family scope.
    """
    family_id = await membership_repo.get_default_family_id_for_user(session, current_user.id)
    if not family_id:
        raise HTTPException(status_code=400, detail="User has no family membership")
    return ScopeSchema(scope_type="family", scope_id=str(family_id))
