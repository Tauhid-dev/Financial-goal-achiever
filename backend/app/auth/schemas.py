from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str

class UserRead(BaseModel):
    id: str
    email: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# New schema for the scopes endpoint
class ScopeItemSchema(BaseModel):
    type: str
    id: str
    name: str | None = None
