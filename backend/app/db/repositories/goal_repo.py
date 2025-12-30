import uuid
from datetime import datetime
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from ..models.goal import Goal

async def create_goal(
    session: AsyncSession,
    family_id: str,
    name: str,
    target_amount: float,
    current_amount: float = 0.0,
    monthly_contribution: float = 0.0,
    target_date: str | None = None,
) -> Goal:
    """Create a Goal row and return the persisted object."""
    goal = Goal(
        id=str(uuid.uuid4()),
        family_id=family_id,
        name=name,
        target_amount=target_amount,
        current_amount=current_amount,
        monthly_contribution=monthly_contribution,
        target_date=target_date,
        created_at=datetime.utcnow(),
    )
    session.add(goal)
    await session.flush()
    return goal

async def list_goals(session: AsyncSession, family_id: str) -> List[Goal]:
    """Return all Goal rows for a family, newest first."""
    stmt = select(Goal).where(Goal.family_id == family_id).order_by(desc(Goal.created_at))
    result = await session.execute(stmt)
    return result.scalars().all()

async def delete_goal(session: AsyncSession, family_id: str, goal_id: str) -> bool:
    """Delete a Goal row; return True if deleted, False if not found."""
    stmt = select(Goal).where(Goal.family_id == family_id).where(Goal.id == goal_id)
    result = await session.execute(stmt)
    goal = result.scalar_one_or_none()
    if not goal:
        return False
    await session.delete(goal)
    await session.flush()
    return True
