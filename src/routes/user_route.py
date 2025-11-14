from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.database import SessionLocal
from src.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from src.services.user_service import (
    create_user, get_user, get_all_users, update_user, delete_user
)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create(user_data: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user_data)


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def read(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found !")
    return user


@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def read_all(db: Session = Depends(get_db)):
    return get_all_users(db)


@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update(user_id: int, updates: UserUpdate, db: Session = Depends(get_db)):
    user = update_user(db, user_id, updates)
    if not user:
        raise HTTPException(status_code=404, detail="User not found !")
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(user_id: int, db: Session = Depends(get_db)):
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found !")
    return {"detail": "User deleted !"}
