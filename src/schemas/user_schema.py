from pydantic import BaseModel, EmailStr, validator

class UserBase(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    username: str
    email: EmailStr
    phone_number: str

class UserCreate(UserBase):
    username: str
    email: EmailStr
    phone_number: str
    password : str

class UserUpdate(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    username: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None

    @validator("username")
    def username_not_empty(cls, value):
        if value is not None and not value.strip():
            raise ValueError("username can not be empty !")
        return value

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
