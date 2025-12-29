from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..services.pipeline import process_pdf
from backend.app.modules.models.schemas import FamilySchema, DocumentSchema
from backend.app.auth.deps import get_current_user
from backend.app.db.models import User
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
async def upload_document(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """
    Accept a PDF upload, store it temporarily, run the processing pipeline,
    then persist results to the database.
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

    # Persist results inside a transaction
    from backend.app.db.repositories.membership_repo import get_default_family_id_for_user

    async with session.begin():
        # Resolve family_id for current user
        family_id = await get_default_family_id_for_user(session, current_user.id)
        if not family_id:
            raise HTTPException(status_code=400, detail="User has no family membership")
        # Create Document row
        doc = await create_document(
            session,
            family_id=family_id,
            filename=file.filename,
            source_type="bank_statement_v1",
        )
        # Bulk insert Transactions
        txn_count = await bulk_create_transactions(
            session,
            document_id=doc.id,
            family_id=doc.family_id,
            txns=pipeline_result.get("transactions_normalized", []),
        )
        # Upsert Monthly Summaries
        summary_count = await upsert_monthly_summaries(
            session,
            family_id=doc.family_id,
            monthly=pipeline_result.get("monthly_summary", {}),
        )

    # Return enriched response
    return {
        "id": doc.id,
        "family_id": doc.family_id,
        "filename": doc.filename,
        "uploaded_at": doc.uploaded_at.isoformat(),
        "transactions_inserted": txn_count,
        "months_upserted": summary_count,
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
