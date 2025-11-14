
from pydantic import BaseModel, EmailStr

class RegisterIn(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    username: str
    email: EmailStr
    phone_number: str
    password: str

class LoginIn(BaseModel):
    username_or_email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshIn(BaseModel):
    refresh_token: str
