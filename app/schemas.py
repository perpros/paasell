from pydantic import BaseModel
from typing import Optional

# Pydantic model for Role
class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int

    class Config:
        orm_mode = True

# Pydantic model for User
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str
    role_id: int

class User(UserBase):
    id: int
    is_active: bool
    role: Role

    class Config:
        orm_mode = True

# Pydantic model for Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
