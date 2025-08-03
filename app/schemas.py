from pydantic import BaseModel
from typing import Optional
from .models import Role

class UserBase(BaseModel):
    username: str
    role: Role

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
