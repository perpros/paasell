from pydantic import BaseModel, EmailStr
from typing import Optional, List

# --- Role Schemas ---
class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    name: Optional[str] = None # Allow partial updates
    description: Optional[str] = None

class RoleInDBBase(RoleBase):
    id: int

    class Config:
        orm_mode = True # Pydantic v1
        # from_attributes = True # Pydantic v2

class Role(RoleInDBBase):
    pass

# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr
    username: str
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    password: str
    # Optionally, allow assigning roles on creation
    # role_ids: Optional[List[int]] = None
    # Or role_names: Optional[List[str]] = None

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None # For password change
    is_active: Optional[bool] = None
    # role_ids: Optional[List[int]] = None
    # Or role_names: Optional[List[str]] = None

class UserInDBBase(UserBase):
    id: int
    # roles: List[Role] = [] # Roles will be loaded via relationship

    class Config:
        orm_mode = True # Pydantic v1
        # from_attributes = True # Pydantic v2

class User(UserInDBBase): # User model for reading (response)
    roles: List[Role] = [] # Eagerly load roles for response

class UserList(BaseModel):
    items: List[User]
    total: int

# --- UserRole Assignment Schema ---
class UserRoleAssign(BaseModel):
    role_name: str # Assign role by name for simplicity for API consumer
    # Or role_id: int


# --- For login, it's better to use OAuth2PasswordRequestForm from FastAPI
# but if you had a JSON body login:
# class UserLogin(BaseModel):
#     username: str # This can be username or email
#     password: str
