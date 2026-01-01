import pytest
from datetime import datetime
from backend.app.modules.models.schemas import DocumentListItemSchema

def test_document_list_item_schema():
    item = DocumentListItemSchema(
        id="doc1",
        family_id="fam1",
        filename="file.pdf",
        uploaded_at=datetime.utcnow(),
        status="processed",
        source_type="pdf",
    )
    assert item.id == "doc1"
    assert item.status == "processed"
    assert item.source_type == "pdf"
