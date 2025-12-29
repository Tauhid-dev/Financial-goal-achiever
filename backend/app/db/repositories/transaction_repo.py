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
    Returns the number of rows inserted.
    """
    if not txns:
        return 0

    objs = []
    for tx in txns:
        obj = Transaction(
            id=str(uuid.uuid4()),
            document_id=document_id,
            family_id=family_id,
            date=tx.get("date"),
            description=tx.get("description", ""),
            amount=tx.get("amount", 0.0),
            direction=tx.get("direction", ""),
            category=tx.get("category", ""),
            subcategory=tx.get("subcategory"),
            confidence=tx.get("confidence", 0.0),
        )
        objs.append(obj)

    session.add_all(objs)
    await session.flush()
    return len(objs)
