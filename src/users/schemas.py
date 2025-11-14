from pydantic import BaseModel, EmailStr, validator
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    manager = "manager"
    user = "user"

class UserBase(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    username: str
    email: EmailStr
    phone_number: str
    role: UserRole = UserRole.user  # 👈 ajout ici

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    username: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    role: UserRole | None = None  # 👈 autoriser la mise à jour du rôle

    @validator("username")
    def username_not_empty(cls, value):
        if value is not None and not value.strip():
            raise ValueError("username cannot be empty!")
        return value

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
