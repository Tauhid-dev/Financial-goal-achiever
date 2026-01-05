from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.auth.deps import get_current_user
from backend.app.db.session import get_async_session
from backend.app.db.models import User
from backend.app.db.repositories.membership_repo import get_default_family_id_for_user, list_user_families
from backend.app.modules.models.schemas import ScopeSchema

router = APIRouter(prefix="/api/scopes", tags=["Scopes"])

@router.get("/scopes", response_model=list[ScopeSchema])
async def list_scopes(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    families = await list_user_families(session, current_user.id)
    return [
        ScopeSchema(id=family_id, type="family", name=family_name)
        for family_id, family_name in families
    ]
