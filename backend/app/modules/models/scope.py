from pydantic import BaseModel
from typing import Literal

class ScopeDTO(BaseModel):
    """
    Lightweight Data Transfer Object representing a scope.
    Currently only supports families (type="family").
    """
    id: str
    type: Literal["family"]
    name: str | None = None
