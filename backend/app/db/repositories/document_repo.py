import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.document import Document

async def create_document(
    session: AsyncSession,
    family_id: str,
    filename: str,
    source_type: str = "bank_statement_v1",
) -> Document:
    """
    Create a Document row with default status "processed".
    Does NOT commit; caller must manage the transaction.
    """
    doc = Document(
        id=str(uuid.uuid4()),
        family_id=family_id,
        filename=filename,
        uploaded_at=datetime.utcnow(),
        status="processed",
        source_type=source_type,
    )
    session.add(doc)
    await session.flush()
    return doc

async def list_documents(session: AsyncSession, family_id: str):
    """
    Return a list of Document rows for the given family,
    ordered by uploaded_at descending.
    """
    stmt = select(Document).where(
        Document.family_id == family_id
    ).order_by(Document.uploaded_at.desc())
    result = await session.execute(stmt)
    return result.scalars().all()
