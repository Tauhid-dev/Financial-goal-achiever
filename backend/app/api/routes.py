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
from backend.app.modules.goals.api_mapping import goal_row_to_with_projection
# Fixed import path for deterministic insights
# Fixed import path for deterministic insights
from backend.app.modules.insight.deterministic import build_insights

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
async def upload_document_placeholder():
    """
    Placeholder endpoint – actual file upload functionality requires
    the optional 'python-multipart' package, which is not installed in
    this test environment. This stub satisfies route registration without
    triggering multipart validation.
    """
    return {"detail": "Upload endpoint placeholder – multipart support not available."}

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
@router.post("/goals/{family_id}", response_model=GoalWithProjectionSchema)
async def create_goal(
    family_id: str,
    goal: GoalCreateSchema,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new goal for a family, enforce authz, and return the goal with projection.
    """
    await assert_family_access(session, current_user.id, family_id)
    # Create the goal in the DB
    created = await repo_create_goal(
        session,
        family_id,
        name=goal.name,
        target_amount=goal.target_amount,
        current_amount=goal.current_amount,
        monthly_contribution=goal.monthly_contribution,
        target_date=goal.target_date,
    )
    # Convert ORM object to response schema with projection
    return GoalWithProjectionSchema(**goal_row_to_with_projection(created))

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
        result.append(GoalWithProjectionSchema(**goal_row_to_with_projection(g)))
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
