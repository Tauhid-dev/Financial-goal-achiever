import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.monthly_summary import MonthlySummary

async def upsert_monthly_summaries(
    session: AsyncSession,
    family_id: str,
    monthly: dict,
) -> int:
    """
    Upsert MonthlySummary rows for each month in the provided dict.
    Input format:
        {
            "2023-01": {"income": ..., "expenses": ..., "savings": ..., "savings_rate": ...},
            ...
        }
    Returns the number of rows upserted/created.
    """
    count = 0
    for month, data in monthly.items():
        stmt = select(MonthlySummary).where(
            MonthlySummary.family_id == family_id,
            MonthlySummary.month == month,
        )
        result = await session.execute(stmt)
        existing = result.scalar_one_or_none()

        if existing:
            existing.income = data.get("income", 0.0)
            existing.expenses = data.get("expenses", 0.0)
            existing.savings = data.get("savings", 0.0)
            existing.savings_rate = data.get("savings_rate", 0.0)
            existing.generated_at = datetime.utcnow()
        else:
            new = MonthlySummary(
                id=str(uuid.uuid4()),
                family_id=family_id,
                month=month,
                income=data.get("income", 0.0),
                expenses=data.get("expenses", 0.0),
                savings=data.get("savings", 0.0),
                savings_rate=data.get("savings_rate", 0.0),
                generated_at=datetime.utcnow(),
            )
            session.add(new)

        count += 1

    await session.flush()
    return count
