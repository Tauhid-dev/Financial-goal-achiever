from typing import List, Optional
from sqlalchemy import select
from ...modules.models.scope import ScopeDTO
from ..models.family import Family
from ..models.membership import Membership
from ..models.user import User

async def list_scopes_for_user(session, user_id: str) -> List[ScopeDTO]:
    """
    Return all families the user belongs to as ScopeDTO objects.
    """
    stmt = (
        select(Family.id, Family.name)
        .join(Membership, Membership.family_id == Family.id)
        .where(Membership.user_id == user_id)
        .order_by(Family.created_at.asc())
    )
    result = await session.execute(stmt)
    return [
        ScopeDTO(id=str(fid), type="family", name=name or "Family")
        for fid, name in result.all()
    ]

async def get_default_scope_for_user(session, user_id: str) -> Optional[ScopeDTO]:
    """
    Return the default family for the user.
    - Prefer User.default_family_id if set.
    - Fallback to the earliest family via membership.
    """
    # Try explicit default on User
    user_res = await session.execute(select(User).where(User.id == user_id))
    user = user_res.scalar_one_or_none()
    if user and user.default_family_id:
        fam_res = await session.execute(
            select(Family.id, Family.name).where(Family.id == user.default_family_id)
        )
        fam = fam_res.first()
        if fam:
            fid, name = fam
            return ScopeDTO(id=str(fid), type="family", name=name or "Family")

    # Fallback to first family via membership
    scopes = await list_scopes_for_user(session, user_id)
    return scopes[0] if scopes else None
