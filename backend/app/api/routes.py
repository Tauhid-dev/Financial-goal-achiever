from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..services.pipeline import process_pdf
from backend.app.modules.models.schemas import FamilySchema, DocumentSchema, MonthlySummarySchema, TransactionSchema
from backend.app.auth.deps import get_current_user
from backend.app.db.models import User
from backend.app.db.session import get_async_session
from backend.app.db.repositories.document_repo import create_document, list_documents
from backend.app.db.repositories.membership_repo import get_default_family_id_for_user
from backend.app.db.repositories.transaction_repo import bulk_create_transactions, list_transactions, top_expense_categories
from backend.app.db.repositories.summary_repo import upsert_monthly_summaries, list_monthly_summaries
from ..api.authz import assert_family_access
from backend.app.db.repositories.goal_repo import create_goal as repo_create_goal, list_goals as repo_list_goals, delete_goal as repo_delete_goal
from backend.app.modules.models.schemas import GoalCreateSchema, GoalWithProjectionSchema
from backend.app.modules.goals.schema import SavingsGoal
from backend.app.modules.goals.projection import project_time_to_goal
from backend.app.modules.insights.deterministic import build_insights

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
@router.get("/summary/{family_id}", response_model=list[MonthlySummarySchema])
async def get_summary(
    family_id: str,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    await assert_family_access(session, current_user.id, family_id)
    rows = await list_monthly_summaries(session, family_id)
    return rows

@router.get("/documents/{family_id}", response_model=list[DocumentSchema])
async def get_documents(
    family_id: str,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    await assert_family_access(session, current_user.id, family_id)
    rows = await list_documents(session, family_id)
    return rows

@router.get("/transactions/{family_id}", response_model=list[TransactionSchema])
async def get_transactions(
    family_id: str,
    month: str | None = None,
    limit: int = 100,
    offset: int = 0,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    await assert_family_access(session, current_user.id, family_id)
    rows = await list_transactions(session, family_id, month=month, limit=limit, offset=offset)
    return rows

# -----------------------------------------------------------------
# Goals
# -----------------------------------------------------------------
@router.post("/goals", response_model=GoalWithProjectionSchema)
async def create_goal(
    goal: GoalCreateSchema,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    # Resolve family_id for current user
    family_id = await get_default_family_id_for_user(session, current_user.id)
    if not family_id:
        raise HTTPException(status_code=400, detail="User has no family membership")
    async with session.begin():
        # Create DB goal row
        db_goal = await repo_create_goal(
            session,
            family_id=family_id,
            name=goal.name,
            target_amount=goal.target_amount,
            current_amount=goal.current_amount,
            monthly_contribution=goal.monthly_contribution,
            target_date=goal.target_date,
        )
    # Build deterministic projection
    savings_goal = SavingsGoal(
        id=db_goal.id,
        family_id=db_goal.family_id,
        name=db_goal.name,
        target_amount=db_goal.target_amount,
        current_amount=db_goal.current_amount,
        monthly_contribution=db_goal.monthly_contribution,
        target_date=db_goal.target_date,
    )
    projection = project_time_to_goal(savings_goal)
    # Return combined schema
    return GoalWithProjectionSchema(
        id=db_goal.id,
        family_id=db_goal.family_id,
        name=db_goal.name,
        target_amount=db_goal.target_amount,
        current_amount=db_goal.current_amount,
        monthly_contribution=db_goal.monthly_contribution,
        target_date=db_goal.target_date,
        projection=projection,
    )

@router.get("/goals/{family_id}", response_model=list[GoalWithProjectionSchema])
async def list_goals(
    family_id: str,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    await assert_family_access(session, current_user.id, family_id)
    db_goals = await repo_list_goals(session, family_id)
    result = []
    for g in db_goals:
        savings_goal = SavingsGoal(
            id=g.id,
            family_id=g.family_id,
            name=g.name,
            target_amount=g.target_amount,
            current_amount=g.current_amount,
            monthly_contribution=g.monthly_contribution,
            target_date=g.target_date,
        )
        projection = project_time_to_goal(savings_goal)
        result.append(
            GoalWithProjectionSchema(
                id=g.id,
                family_id=g.family_id,
                name=g.name,
                target_amount=g.target_amount,
                current_amount=g.current_amount,
                monthly_contribution=g.monthly_contribution,
                target_date=g.target_date,
                projection=projection,
            )
        )
    return result

@router.delete("/goals/{family_id}/{goal_id}", response_model=dict)
async def delete_goal(
    family_id: str,
    goal_id: str,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    await assert_family_access(session, current_user.id, family_id)
    async with session.begin():
        ok = await repo_delete_goal(session, family_id, goal_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Goal not found")
    return {"deleted": True}

# -----------------------------------------------------------------
# Insights – uses the InsightService
# -----------------------------------------------------------------
@router.get("/insights/{family_id}")
async def get_insights(
    family_id: str,
    month: str | None = None,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    await assert_family_access(session, current_user.id, family_id)

    # Load all monthly summaries once
    summaries = await list_monthly_summaries(session, family_id)

    # Determine month to use
    if month:
        month_to_use = month
    else:
        month_to_use = summaries[0].month if summaries else None

    # Fetch latest summary dict (or None)
    latest_summary = None
    if month_to_use:
        for s in summaries:
            if s.month == month_to_use:
                latest_summary = {
                    "month": s.month,
                    "income": s.income,
                    "expenses": s.expenses,
                    "savings": s.savings,
                    "savings_rate": s.savings_rate,
                }
                break

    # Top expense categories
    top_cats = await top_expense_categories(session, family_id, month_to_use)

    # Build deterministic insights
    return build_insights(latest_summary, top_cats)
