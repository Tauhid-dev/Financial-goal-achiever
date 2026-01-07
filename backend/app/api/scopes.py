from fastapi import APIRouter, Depends
from typing import List
from backend.app.auth.deps import get_current_user
from backend.app.db.session import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.models.user import User
from backend.app.auth.schemas import ScopeItemSchema
from backend.app.db.models.membership import Membership
from backend.app.db.models.family import Family
from sqlalchemy import select

router = APIRouter(prefix="/api/me", tags=["Scopes"])

@router.get("/scopes", response_model=List[ScopeItemSchema])
async def get_scopes(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
) -> List[ScopeItemSchema]:
    """
    Return all scopes (currently families) the authenticated user belongs to.
    """
    stmt = (
        select(Membership, Family)
        .join(Family, Membership.family_id == Family.id)
        .where(Membership.user_id == current_user.id)
        .order_by(Membership.created_at.asc())
    )
    result = await session.execute(stmt)
    scopes: List[ScopeItemSchema] = []
    for membership, family in result.all():
        scopes.append(
            ScopeItemSchema(
                type="family",
                id=str(family.id),
                name=family.name or "Family"
            )
        )
    return scopes
