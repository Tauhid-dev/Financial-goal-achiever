from sqlalchemy import select, exists
from ..models.membership import Membership

async def add_member(session, user_id: str, family_id: str, role: str = "owner") -> Membership:
    """
    Add a membership linking a user to a family.
    If the membership already exists, return the existing one.
    """
    result = await session.execute(
        select(Membership).where(Membership.user_id == user_id, Membership.family_id == family_id)
    )
    existing = result.scalar_one_or_none()
    if existing:
        return existing

    membership = Membership(user_id=user_id, family_id=family_id, role=role)
    session.add(membership)
    await session.flush()
    return membership

async def get_default_family_id_for_user(session, user_id: str):
    """
    Return the first family_id the user belongs to, ordered by creation.
    """
    result = await session.execute(
        select(Membership.family_id)
        .where(Membership.user_id == user_id)
        .order_by(Membership.created_at.asc())
    )
    row = result.first()
    return row[0] if row else None

async def list_user_families(session, user_id: str):
    """
    Return a list of (family_id, family_name) tuples for the given user.
    """
    stmt = (
        select(Membership.family_id, Family.name)
        .join(Family, Family.id == Membership.family_id)
        .where(Membership.user_id == user_id)
    )
    result = await session.execute(stmt)
    return result.all()

async def user_belongs_to_family(session, user_id: str, family_id: str) -> bool:
    """
    Return True if a membership exists for the given user and family.
    """
    result = await session.execute(
        select(exists().where(Membership.user_id == user_id, Membership.family_id == family_id))
    )
    return result.scalar()
