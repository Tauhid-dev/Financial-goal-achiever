import re
from typing import List, Dict
from .base import BaseDocumentParser

class BankStatementParserV1(BaseDocumentParser):
    """
    Very simple, defensive bank‑statement parser.
    Detects generic keywords and extracts lines that look like:
        DATE DESCRIPTION AMOUNT
    The amount may be prefixed with a minus sign for debits.
    """

    KEYWORDS = {"balance", "transaction", "debit", "credit"}

    def can_parse(self, text: str) -> bool:
        lowered = text.lower()
        return any(keyword in lowered for keyword in self.KEYWORDS)

    def extract(self, text: str) -> List[Dict]:
        """
        Extract minimal transaction data.
        Returns a list of dicts with keys: date, description, amount.
        """
        results: List[Dict] = []
        # Simple line‑by‑line regex: date (YYYY‑MM‑DD or similar) then description then amount
        line_regex = re.compile(
            r"""(?P<date>\d{4}[-/]\d{2}[-/]\d{2})\s+   # date
                (?P<description>.+?)\s+                # description
                (?P<amount>-?\d+(?:\.\d{2})?)          # amount, optional minus
            """,
            re.VERBOSE,
        )
        for line in text.splitlines():
            match = line_regex.search(line)
            if match:
                date = match.group("date")
                description = match.group("description").strip()
                amount = float(match.group("amount"))
                results.append(
                    {
                        "date": date,
                        "description": description,
                        "amount": amount,
                    }
                )
        return results
