from typing import Optional
from .base import BaseDocumentParser
from .bank_statement_parser_v1 import BankStatementParserV1

# List of available parsers – order matters (first match wins)
PARSERS = [BankStatementParserV1()]

def get_parser_for_text(text: str) -> Optional[BaseDocumentParser]:
    """
    Return the first parser that reports it can handle the given text,
    or None if no parser matches.
    """
    for parser in PARSERS:
        if parser.can_parse(text):
            return parser
    return None
