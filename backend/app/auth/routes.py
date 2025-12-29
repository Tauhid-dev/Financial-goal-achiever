from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..db.session import get_async_session
from ..db.models import User
from .security import hash_password, verify_password
from .jwt import create_access_token
from .schemas import UserCreate, UserRead, Token
from .deps import get_current_user
from ..core.config import Config

router = APIRouter(prefix="/api/auth", tags=["auth"])
settings = Config()

@router.post("/register", response_model=UserRead)
async def register(
    user: UserCreate,
    session: AsyncSession = Depends(get_async_session),
):
    # Check if email already exists
    result = await session.execute(select(User).where(User.email == user.email))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(
        email=user.email,
        password_hash=hash_password(user.password),
    )
    session.add(new_user)
    await session.flush()
    await session.commit()
    return UserRead.from_orm(new_user)

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = create_access_token(subject=user.email)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserRead)
async def read_me(current_user: User = Depends(get_current_user)):
    return UserRead.from_orm(current_user)
