from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.users import schemas as user_schemas # Local schemas
from app.auth.schemas import UserCreate as AuthUserCreate # Schema for creation from auth
from app.dependencies import get_db, RoleChecker, get_current_active_user
from app.models import User as UserModel
from app.models import Role as RoleModel

router = APIRouter()

# RoleChecker instance for Admin-only access
admin_only = RoleChecker(["Admin"])

@router.post("/", response_model=user_schemas.User, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(admin_only)])
async def create_user(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: AuthUserCreate # Using the one defined in auth.schemas for consistency with login etc.
                            # Or user_schemas.UserCreate if it's different and preferred here
    # current_admin: UserModel = Depends(admin_only) # Not strictly needed if just using dependency for protection
) -> Any:
    """
    Create new user. (Admin only)
    """
    existing_user_by_email = await crud.user.get_by_email(db, email=user_in.email)
    if existing_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists.",
        )
    existing_user_by_username = await crud.user.get_by_username(db, username=user_in.username)
    if existing_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this username already exists.",
        )

    user = await crud.user.create(db=db, obj_in=user_in)

    # Optionally, assign a default role like "User" if not specified, or handle via UserCreate schema
    # default_role_name = "User"
    # role_obj = await crud.role.get_by_name(db, name=default_role_name)
    # if role_obj:
    #     user = await crud.user.assign_role_to_user(db, user=user, role=role_obj)
    # else:
    #     # Log a warning or handle missing default role
    #     pass

    # To return roles correctly, we might need to refresh or load them if not done by create
    # The response_model user_schemas.User expects roles.
    # Let's ensure the user object returned has roles loaded.
    # crud.user.create doesn't add roles by default.
    # For a newly created user, roles list will be empty unless logic is added.
    # We can fetch the user again with roles.
    created_user_with_roles = await crud.user.get(db, id=user.id) # This loads roles
    return created_user_with_roles


@router.post("/{user_id}/roles", response_model=user_schemas.User,
              dependencies=[Depends(admin_only)])
async def assign_role_to_user(
    user_id: int,
    role_assignment: user_schemas.UserRoleAssign, # Request body with role_name
    db: AsyncSession = Depends(get_db),
    # current_admin: UserModel = Depends(admin_only) # For admin context if needed
):
    """
    Assign a role to a user. (Admin only)
    """
    user = await crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    role_to_assign = await crud.role.get_by_name(db, name=role_assignment.role_name)
    if not role_to_assign:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Role '{role_assignment.role_name}' not found.")

    updated_user = await crud.user.assign_role_to_user(db, user=user, role=role_to_assign)
    return updated_user


@router.get("/me", response_model=user_schemas.User)
async def read_users_me(
    current_user: UserModel = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db) # Added db session for potentially reloading with all roles
):
    """
    Get current user's details.
    """
    # The current_user from get_current_active_user might not have roles fully populated
    # depending on how it was loaded. Let's ensure roles are loaded for the response.
    user_with_roles = await crud.user.get(db, id=current_user.id) # crud.user.get loads roles
    if not user_with_roles: # Should not happen if token is valid
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_with_roles


@router.get("/", response_model=List[user_schemas.User], dependencies=[Depends(admin_only)])
async def read_users(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    # current_admin: UserModel = Depends(admin_only) # For admin context
):
    """
    Retrieve users. (Admin only)
    This is a basic version. In a real app, you'd want pagination.
    """
    # This is a simplified get_multi. A real version would be in crud_user.
    from sqlalchemy.future import select
    result = await db.execute(select(UserModel).offset(skip).limit(limit).options(selectinload(UserModel.roles)))
    users = result.scalars().all()
    return users

# Placeholder for other user management endpoints (GET by ID, PUT, DELETE)
# @router.get("/{user_id}", response_model=user_schemas.User, dependencies=[Depends(admin_only)])
# async def read_user_by_id(...): ...

# @router.put("/{user_id}", response_model=user_schemas.User, dependencies=[Depends(admin_only)])
# async def update_user(...): ...

# @router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(admin_only)])
# async def delete_user(...): ...
