try:
    from .orm import (
        Base,
        Family,
        FamilyMember,
        Document,
        Transaction,
        Goal,
        MonthlySummary,
    )
except ModuleNotFoundError:
    # Fallback to stub definitions when SQLAlchemy is unavailable
    from .orm_stub import (
        Base,
        Family,
        FamilyMember,
        Document,
        Transaction,
        Goal,
        MonthlySummary,
    )

from .schemas import (
    FamilySchema,
    FamilyMemberSchema,
    DocumentSchema,
    TransactionSchema,
    GoalSchema,
    MonthlySummarySchema,
)
