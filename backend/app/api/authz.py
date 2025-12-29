from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.repositories.membership_repo import user_belongs_to_family

async def assert_family_access(session: AsyncSession, user_id: str, family_id: str) -> None:
    """
    Verify that the given user belongs to the specified family.
    Raises HTTPException(403) if the user is not a member.
    """
    allowed = await user_belongs_to_family(session, user_id, family_id)
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
