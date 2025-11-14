from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.auth.schemas import RegisterIn, LoginIn, TokenResponse, RefreshIn
from src.auth.services import get_db, register_user, authenticate_user, create_pair_and_store, verify_refresh_token_in_db, revoke_refresh_token
from src.auth.services import get_current_user, User

router = APIRouter()

@router.post("/register", response_model=TokenResponse)
def register(user_data: RegisterIn, db: Session = Depends(get_db)):
    user = register_user(db, user_data)
    return create_pair_and_store(db, user)

@router.post("/login", response_model=TokenResponse)
def login(data: LoginIn, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.username_or_email, data.password)
    return create_pair_and_store(db, user)

@router.post("/refresh", response_model=TokenResponse)
def refresh(data: RefreshIn, db: Session = Depends(get_db)):
    db_token = verify_refresh_token_in_db(db, data.refresh_token)
    user = db.query(User).filter(User.id == db_token.user_id).first()
    revoke_refresh_token(db, db_token)  # rotation
    return create_pair_and_store(db, user)

@router.post("/logout")
def logout(data: RefreshIn, db: Session = Depends(get_db)):
    db_token = verify_refresh_token_in_db(db, data.refresh_token)
    revoke_refresh_token(db, db_token)
    return {"detail": "Refresh token revoked"}

@router.get("/me", response_model=dict)
def me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "username": current_user.username, "email": current_user.email}
