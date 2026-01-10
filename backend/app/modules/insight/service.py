from typing import Mapping, Any, Optional

from .default_provider import DeterministicProvider
from .provider import InsightProvider

class InsightService:
    """
    Generates a plain‑English insight from a financial summary and a goal result.
    An external provider can be injected at runtime; otherwise the deterministic
    placeholder is used.
    """

    def __init__(self, provider: Optional[InsightProvider] = None):
        self.provider = provider or DeterministicProvider()

    def explain(
        self,
        financial_summary: Mapping[str, Any],
        goal_result: Mapping[str, Any],
    ) -> str:
        """
        Return a human‑readable explanation with optional suggestions.
        The method does not touch the database and never fabricates numbers.
        """
        return self.provider.generate(financial_summary, goal_result)
