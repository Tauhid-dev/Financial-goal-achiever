from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from ..services.pipeline import process_pdf
from typing import List

from ..modules.models.schemas import FamilySchema, DocumentSchema
from ..modules.normalize.schemas import NormalizedTransaction
from ..modules.goals.schemas import GoalInput, GoalResult
from ..modules.insight.service import InsightService

# Service imports (thin wrappers around core logic)
from ..modules.ingest.bank_statement_parser_v1 import BankStatementParserV1
from ..modules.normalize.normalizer import TransactionNormalizer
from ..modules.goals.engine import GoalEngine

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
@router.get("/summary/{family_id}", response_model=List[NormalizedTransaction])
async def get_summary(family_id: str):
    # TODO: integrate with pipeline or DB to return actual summary.
    # Currently returns an empty list as a placeholder.
    raw = []  # In a real system this would be fetched from DB
    normalized = TransactionNormalizer.batch_normalize(raw)
    return normalized

# -----------------------------------------------------------------
# Goals
# -----------------------------------------------------------------
@router.post("/goals", response_model=GoalResult)
async def create_goal(goal: GoalInput):
    result = GoalEngine.evaluate(goal)
    return result

# -----------------------------------------------------------------
# Insights – uses the InsightService
# -----------------------------------------------------------------
@router.get("/insights/{family_id}", response_model=str)
async def get_insights(family_id: str):
    # Placeholder financial summary and goal result
    financial_summary = {
        "income": 5000.0,
        "surplus": 500.0,
        "savings_rate": 10.0,
    }
    goal_result = {
        "required_savings_per_month": 400.0,
        "feasible": True,
    }
    service = InsightService()
    return service.explain(financial_summary, goal_result)
