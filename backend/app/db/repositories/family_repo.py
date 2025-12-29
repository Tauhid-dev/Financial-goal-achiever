from sqlalchemy import select
from ..models.family import Family

async def create_family(session, name: str = "My Family") -> Family:
    """
    Create a new Family row.
    """
    family = Family(name=name)
    # If Family model had a name column, you could set it here:
    # family.name = name
    session.add(family)
    await session.flush()
    return family

async def get_family_by_id(session, family_id: str):
    result = await session.execute(select(Family).where(Family.id == family_id))
    return result.scalar_one_or_none()
