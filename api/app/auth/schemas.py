from pydantic import BaseModel, EmailStr
from typing import Optional, List

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    user_id: Optional[int] = None
    role: Optional[str] = None # Or List[str] if multiple roles are embedded
    # sub: Optional[str] = None # If using 'sub' for username or id
    exp: Optional[int] = None

# Schemas for user creation and reading, might live in users.schemas but useful here too
class UserBase(BaseModel): # This could be imported from users.schemas if identical
    email: EmailStr
    username: str
    is_active: Optional[bool] = True # Added for consistency

class UserCreate(UserBase): # Used by POST /users and potentially others
    password: str

class UserInDBBase(UserBase): # This could be imported from users.schemas if identical
    id: int
    is_active: bool
    # roles: List[RoleSchema] # Define RoleSchema if you want to nest role details

    class Config:
        orm_mode = True # Pydantic V1, for V2 use from_attributes = True

# Minimal Role schema for embedding in User or Token
class Role(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True # Pydantic V1, for V2 use from_attributes = True

class UserWithRoles(UserInDBBase):
    roles: List[Role] = []

# For login form (OAuth2PasswordRequestForm is used by FastAPI for this)
# class LoginRequest(BaseModel):
#     username: str # This will typically be email or username
#     password: str
