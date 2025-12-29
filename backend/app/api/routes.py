from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..services.pipeline import process_pdf
from backend.app.modules.models.schemas import FamilySchema, DocumentSchema
from backend.app.db.session import get_async_session
from backend.app.db.repositories.document_repo import create_document
from backend.app.db.repositories.transaction_repo import bulk_create_transactions
from backend.app.db.repositories.summary_repo import upsert_monthly_summaries

router = APIRouter(prefix="/api", tags=["Family Finance"])

# -----------------------------------------------------------------
# Families
# -----------------------------------------------------------------
@router.post("/families", response_model=FamilySchema)
async def create_family(family: FamilySchema):
    # Placeholder – simply echo the payload
    return family

# -----------------------------------------------------------------
# Document upload (PDF)
# -----------------------------------------------------------------
@router.post("/documents/upload", response_model=DocumentSchema)
async def upload_document(file: UploadFile = File(...)):
    """
    Accept a PDF upload, store it temporarily, run the processing pipeline,
    then delete the temporary file. Returns the pipeline result alongside
    minimal document metadata.
    """
    import os
    import tempfile

    # Write uploaded file to a temporary location
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            content = await file.read()
            tmp.write(content)
            temp_path = tmp.name

        # Run the pure pipeline orchestrator
        pipeline_result = process_pdf(temp_path)

    finally:
        # Ensure the temporary file is removed
        if "temp_path" in locals() and os.path.exists(temp_path):
            os.remove(temp_path)

    # Return document metadata plus pipeline output (as a dict)
    return {
        "id": "placeholder-id",
        "family_id": "placeholder-family",
        "filename": file.filename,
        "uploaded_at": "1970-01-01T00:00:00Z",
        "pipeline_result": pipeline_result,
    }

# -----------------------------------------------------------------
# Summary endpoint – uses normalization layer
# -----------------------------------------------------------------
@router.get("/summary/{family_id}")
async def get_summary(family_id: str):
    raise HTTPException(status_code=501, detail="Not wired yet. Use /documents/upload pipeline.")

# -----------------------------------------------------------------
# Goals
# -----------------------------------------------------------------
@router.post("/goals")
async def create_goal(goal: dict):
    raise HTTPException(status_code=501, detail="Not wired yet. Use /documents/upload pipeline.")

# -----------------------------------------------------------------
# Insights – uses the InsightService
# -----------------------------------------------------------------
@router.get("/insights/{family_id}")
async def get_insights(family_id: str):
    raise HTTPException(status_code=501, detail="Not wired yet. Use /documents/upload pipeline.")
