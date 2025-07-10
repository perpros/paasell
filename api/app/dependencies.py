from typing import List, Optional, Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import decode_token
from app.crud import user as crud_user # Renamed import for clarity
from app.models import User as UserModel # Renamed import for clarity
from app.auth import schemas as auth_schemas # Renamed import for clarity
from app.database import get_db

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    async def __call__(self,
                       db: AsyncSession = Depends(get_db),
                       token: str = Depends(reusable_oauth2)) -> UserModel:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        payload = decode_token(token)
        if payload is None: # Token decoding failed (e.g. expired, invalid)
            raise credentials_exception

        user_id: Optional[int] = payload.get("user_id")
        # token_role: Optional[str] = payload.get("role") # Role from token

        if user_id is None:
            raise credentials_exception

        user = await crud_user.get(db, id=user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

        # Verify role:
        # Option 1: Use role from token (faster, but can be stale if roles change and token is long-lived)
        # if token_role not in self.allowed_roles:
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail=f"User with role '{token_role}' not authorized for this endpoint. Requires one of: {self.allowed_roles}",
        #     )

        # Option 2: Fetch fresh roles from DB (more secure for role changes)
        user_roles_from_db = await crud_user.get_user_roles(user)
        if not any(role_name in self.allowed_roles for role_name in user_roles_from_db):
            # If there are no common roles between user's roles and allowed roles
            if not self.allowed_roles: # If allowed_roles is empty, means any authenticated user is fine
                return user # Or handle as per specific logic for "any authenticated user"

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User roles {user_roles_from_db} not authorized. Requires one of: {self.allowed_roles}",
            )

        return user


# Dependency to get current active user without role check (just valid token)
async def get_current_active_user(
    db: Annotated[AsyncSession, Depends(get_db)], # Using Annotated for newer FastAPI/Pydantic
    token: Annotated[str, Depends(reusable_oauth2)],
) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception

    user_id: Optional[int] = payload.get("user_id")
    if user_id is None:
        raise credentials_exception

    user = await crud_user.get(db, id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

# Example usage for an endpoint requiring 'Admin' role:
# from app.dependencies import RoleChecker
# @router.get("/admin-only", dependencies=[Depends(RoleChecker(["Admin"]))])
# async def get_admin_info(current_user: UserModel = Depends(get_current_active_user)):
#     return {"message": "Admin info", "user": current_user.username}

# For just authenticated user:
# @router.get("/me")
# async def read_users_me(current_user: UserModel = Depends(get_current_active_user)):
#     return current_user
