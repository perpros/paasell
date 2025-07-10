from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud # Updated import
from app.auth import schemas as auth_schemas # Renamed for clarity
from app.core.config import settings
from app.core.security import create_access_token
from app.database import get_db
from app.models import User # For type hinting

router = APIRouter()

@router.post("/login", response_model=auth_schemas.Token)
async def login_for_access_token(
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    Uses username (which can be email or actual username) and password.
    """
    # In OAuth2PasswordRequestForm, 'username' field is used for the identifier (email/username)
    user = await crud.user.authenticate(db, username_or_email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Determine user's role for the token.
    # For simplicity, using the first role. This might need refinement
    # if a user can have multiple roles and a "primary" or "session" role is needed.
    user_roles = await crud.user.get_user_roles(user) # Fetches roles if not already loaded or if needed fresh
    # Fallback role if user has no roles assigned, though this should ideally not happen for active users.
    # Or, raise an error if no role is found and a role is mandatory for login.
    # For now, let's assume a user who can log in will have at least one role.
    # If user.roles isn't populated by authenticate, we might need to fetch them:
    # loaded_user = await crud.user.get(db, id=user.id) # This would load roles based on crud_user.get

    # Assuming user.roles is populated by the authenticate method due to selectinload in get_by_username/email
    primary_role_name = user_roles[0] if user_roles else "User" # Default to "User" or handle as error

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    token_data = {
        "user_id": user.id,
        "role": primary_role_name, # Add role to token payload as per AUTH-01
        "sub": user.username # Standard 'sub' claim, can be username or user.id
    }

    access_token = create_access_token(
        subject=token_data, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
