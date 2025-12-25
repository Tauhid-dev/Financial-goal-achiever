from abc import ABC, abstractmethod
from typing import List, Dict

class BaseDocumentParser(ABC):
    """
    Abstract base class for document parsers.
    Implementations must provide `can_parse` and `extract` methods.
    """

    @abstractmethod
    def can_parse(self, text: str) -> bool:
        """Return True if this parser can handle the given text."""
        ...

    @abstractmethod
    def extract(self, text: str) -> List[Dict]:
        """
        Extract structured data from the given text.
        Returns a list of dictionaries representing raw transactions.
        """
        ...
