from sqlalchemy.orm import Session
from fastapi import HTTPException
from .models import User
from .schemas import UserCreate, UserUpdate
from pydantic import EmailStr

def get_user_by_identifier(db: Session, email: EmailStr, username: str, phone_number: str):
    if email:
        user = db.query(User).filter(User.email == email).first()
        if user: return user
    if username:
        user = db.query(User).filter(User.username == username).first()
        if user: return user
    if phone_number:
        user = db.query(User).filter(User.phone_number == phone_number).first()
        if user: return user
    return None

def create_user(db: Session, user_data: UserCreate) -> User:
    existing_user = get_user_by_identifier(db, user_data.email, user_data.username, user_data.phone_number)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email, username, or phone already registered!")

    hashed_password = User.hash_password(user_data.password)
    new_user = User(
        firstname=user_data.firstname,
        lastname=user_data.lastname,
        email=user_data.email,
        username=user_data.username,
        phone_number=user_data.phone_number,
        hashed_password=hashed_password,
        role="user"  # 👈 nouveau champ
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def get_all_users(db: Session):
    return db.query(User).all()

def update_user(db: Session, user_id: int, updates: UserUpdate) -> User | None:
    user = get_user(db, user_id)
    if not user: return None
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int) -> bool:
    user = get_user(db, user_id)
    if not user: return False
    db.delete(user)
    db.commit()
    return True
