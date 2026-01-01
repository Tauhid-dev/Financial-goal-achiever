import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.transaction import Transaction

async def bulk_create_transactions(
    session: AsyncSession,
    document_id: str,
    family_id: str,
    txns: list[dict],
) -> int:
    """
    Bulk insert Transaction rows linked to a Document.
    - Guarantees a non‑null date (defaults to "1970-01-01").
    - Guarantees amount is a float.
    - Guarantees direction is "income" or "expense"; if missing, infer from amount sign.
    Returns the number of rows inserted.
    """
    if not txns:
        return 0

    objs = []
    for tx in txns:
        # Ensure required fields have safe defaults
        tx_date = tx.get("date") or "1970-01-01"
        tx_amount = float(tx.get("amount", 0.0))
        tx_direction = tx.get("direction")
        if tx_direction not in ("income", "expense"):
            # Infer direction from amount sign
            tx_direction = "income" if tx_amount >= 0 else "expense"

        obj = Transaction(
            id=str(uuid.uuid4()),
            document_id=document_id,
            family_id=family_id,
            date=tx_date,
            description=tx.get("description", ""),
            amount=tx_amount,
            direction=tx_direction,
            category=tx.get("category", ""),
            subcategory=tx.get("subcategory"),
            confidence=tx.get("confidence", 0.0),
        )
        objs.append(obj)

    session.add_all(objs)
    await session.flush()
    return len(objs)


async def list_transactions(
    session: AsyncSession,
    family_id: str,
    month: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[Transaction]:
    """
    List transactions for a family, optionally filtered by month.
    """
    from sqlalchemy import select
    query = select(Transaction).where(Transaction.family_id == family_id)
    if month:
        query = query.where(Transaction.date.like(f"{month}%"))
    query = query.order_by(Transaction.date.desc()).limit(limit).offset(offset)
    result = await session.execute(query)
    return result.scalars().all()


async def top_expense_categories(
    session: AsyncSession,
    family_id: str,
    month: str | None = None,
) -> list[dict]:
    """
    Get top 10 expense categories by total amount for a family.
    """
    from sqlalchemy import select, func
    query = select(
        Transaction.category,
        func.sum(Transaction.amount).label("total")
    ).where(
        Transaction.family_id == family_id,
        Transaction.direction == "expense"
    )
    if month:
        query = query.where(Transaction.date.like(f"{month}%"))
    query = query.group_by(Transaction.category).order_by(func.sum(Transaction.amount).desc()).limit(10)
    result = await session.execute(query)
    return [{"category": row.category, "total": row.total} for row in result.all()]
