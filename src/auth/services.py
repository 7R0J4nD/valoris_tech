import hashlib
import uuid
from datetime import datetime, timedelta
from typing import Tuple

from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from core.config import settings
from src.db.database import SessionLocal
from src.users.models import User
from .models import RefreshToken
from .schemas import RegisterIn
from src.users.services import get_user_by_identifier, create_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

def _now(): return datetime.utcnow()

def create_access_token(subject: int, expires_delta: timedelta | None = None) -> Tuple[str, dict]:
    expire = _now() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    jti = str(uuid.uuid4())
    payload = {"sub": str(subject), "exp": expire, "jti": jti, "type": "access"}
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt, {"jti": jti, "exp": expire}

def create_refresh_token(subject: int, expires_delta: timedelta | None = None) -> Tuple[str, dict]:
    expire = _now() + (expires_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
    jti = str(uuid.uuid4())
    payload = {"sub": str(subject), "exp": expire, "jti": jti, "type": "refresh"}
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt, {"jti": jti, "exp": expire}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = decode_token(token)
    if payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not an access token")
    user_id = int(payload.get("sub"))
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

def authenticate_user(db: Session, username_or_email: str, password: str) -> User:
    user = db.query(User).filter((User.email == username_or_email) | (User.username == username_or_email)).first()
    if not user or not user.verify_password(password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    return user

def register_user(db: Session, user_data: RegisterIn) -> User:
    existing_user = get_user_by_identifier(db, user_data.email, user_data.username, user_data.phone_number)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email, username or phone number already registered!")
    return create_user(db, user_data)

def store_refresh_token(db: Session, user: User, refresh_token: str, jti: str, expires_at: datetime):
    token_hash = _hash_token(refresh_token)
    db_token = RefreshToken(
        jti=jti, token_hash=token_hash, user_id=user.id,
        expires_at=expires_at, revoked=False
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def verify_refresh_token_in_db(db: Session, token: str):
    payload = decode_token(token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not a refresh token")
    jti = payload.get("jti")
    token_hash = _hash_token(token)
    db_token = db.query(RefreshToken).filter(RefreshToken.jti == jti).first()
    if not db_token or db_token.revoked or db_token.token_hash != token_hash or db_token.expires_at < _now():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    return db_token

def revoke_refresh_token(db: Session, db_token):
    db_token.revoked = True
    db.commit()

def create_pair_and_store(db: Session, user: User):
    access_token, _ = create_access_token(subject=user.id)
    refresh_token, refresh_meta = create_refresh_token(subject=user.id)
    store_refresh_token(db, user, refresh_token, refresh_meta["jti"], refresh_meta["exp"])
    return {"access_token": access_token, "refresh_token": refresh_token}
