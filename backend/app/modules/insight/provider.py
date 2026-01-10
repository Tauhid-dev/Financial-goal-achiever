from abc import ABC, abstractmethod
from typing import Any, Mapping

class InsightProvider(ABC):
    """
    Abstract provider that generates a plain‑English insight.
    Implementations must not perform DB access or external calls.
    """

    @abstractmethod
    def generate(
        self,
        financial_summary: Mapping[str, Any],
        goal_result: Mapping[str, Any],
    ) -> str:
        """Return a human‑readable explanation."""
        raise NotImplementedError
