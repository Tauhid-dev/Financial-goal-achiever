from collections import defaultdict
from datetime import date
from typing import List, Mapping, Dict, Any

from ..normalize.schemas import NormalizedTransaction
from .constants import FIXED_EXPENSE_KEYWORDS, CHILD_SPEND_KEYWORDS


class FamilyFinanceAnalyzer:
    """
    Service that aggregates a list of NormalizedTransaction objects
    into a per‑family, per‑month financial summary.
    """

    @staticmethod
    def _is_fixed(description: str) -> bool:
        lowered = description.lower()
        return any(word in lowered for word in FIXED_EXPENSE_KEYWORDS)

    @staticmethod
    def _is_child_related(description: str) -> bool:
        lowered = description.lower()
        return any(word in lowered for word in CHILD_SPEND_KEYWORDS)

    @classmethod
    def analyze(
        cls, transactions: List[NormalizedTransaction]
    ) -> List[Dict[str, Any]]:
        """
        Returns a list of monthly summary dicts, one per family.
        Each dict contains:
            - family (str)
            - month (YYYY‑MM)
            - income (float)
            - fixed_expenses (float)
            - variable_expenses (float)
            - surplus (float)
            - savings_rate (float, 0‑100)
            - child_spend_pct (float, 0‑100)
        """
        # Group by (family, month)
        groups: Dict[tuple, List[NormalizedTransaction]] = defaultdict(list)
        for tx in transactions:
            month_key = tx.date.strftime("%Y-%m")
            groups[(tx.member, month_key)].append(tx)

        summaries: List[Dict[str, Any]] = []
        for (family, month), txs in groups.items():
            income = sum(tx.amount for tx in txs if tx.amount > 0)
            expenses = -sum(tx.amount for tx in txs if tx.amount < 0)  # make positive

            fixed = sum(
                -tx.amount
                for tx in txs
                if tx.amount < 0 and cls._is_fixed(tx.description or "")
            )
            variable = expenses - fixed

            surplus = income - expenses
            savings_rate = (surplus / income * 100) if income else 0.0

            child_spend = sum(
                -tx.amount
                for tx in txs
                if tx.amount < 0 and cls._is_child_related(tx.description or "")
            )
            child_spend_pct = (child_spend / expenses * 100) if expenses else 0.0

            summaries.append(
                {
                    "family": family,
                    "month": month,
                    "income": round(income, 2),
                    "fixed_expenses": round(fixed, 2),
                    "variable_expenses": round(variable, 2),
                    "surplus": round(surplus, 2),
                    "savings_rate": round(savings_rate, 2),
                    "child_spend_pct": round(child_spend_pct, 2),
                }
            )
        return summaries
