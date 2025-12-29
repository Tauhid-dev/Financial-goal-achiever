import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
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
