from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, status
from ..core.config import Config

JWT_ALGORITHM = "HS256"

def create_access_token(subject: str, secret: str | None = None, expires_minutes: int = 60) -> str:
    if not secret:
        raise RuntimeError("JWT secret is required but not provided")
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, secret, algorithm=JWT_ALGORITHM)

def decode_access_token(token: str, secret: str) -> dict:
    try:
        payload = jwt.decode(token, secret, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
