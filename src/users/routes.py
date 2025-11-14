from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.database import SessionLocal
from .schemas import UserUpdate, UserResponse
from .services import update_user, delete_user
from src.auth.services import get_current_user, User as AuthUser

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.put("/", response_model=UserResponse)
def update(updates: UserUpdate, db: Session = Depends(get_db), current_user: AuthUser = Depends(get_current_user)):
    user = update_user(db, current_user.id, updates)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(user_id: int, db: Session = Depends(get_db), current_user: AuthUser = Depends(get_current_user)):
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}
