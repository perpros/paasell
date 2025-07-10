import pytest
from httpx import AsyncClient
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud import user as crud_user, role as crud_role
from app.auth.schemas import UserCreate # Assuming UserCreate is used for creating users
from app.core.security import get_password_hash # For creating user directly

# Mark all tests in this module as asyncio
pytestmark = pytest.mark.asyncio

async def test_read_root(async_client: AsyncClient):
    response = await async_client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hello World from FastAPI Backend!"}

async def test_successful_login(async_client: AsyncClient, db_session: AsyncSession):
    # 1. Create a user and a role directly in the database for testing
    test_username = "testuser_login"
    test_email = "testuser_login@example.com"
    test_password = "testpassword"

    # Create Role if it doesn't exist (or ensure it does via a fixture)
    admin_role = await crud_role.get_by_name(db=db_session, name="Admin")
    if not admin_role:
        admin_role = await crud_role.create(db=db_session, name="Admin", description="Admin role for tests")

    user_in_db = await crud_user.get_by_username(db=db_session, username=test_username)
    if not user_in_db:
        user_in = UserCreate(username=test_username, email=test_email, password=test_password)
        user_in_db = await crud_user.create(db=db_session, obj_in=user_in)
        # Assign role
        await crud_user.assign_role_to_user(db=db_session, user=user_in_db, role=admin_role)

    await db_session.commit() # Ensure user and role are committed before login attempt

    # 2. Attempt to login
    login_data = {
        "username": test_username, # This is the identifier (username or email)
        "password": test_password
    }
    response = await async_client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)

    # 3. Assertions
    assert response.status_code == status.HTTP_200_OK
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

    # Optionally, decode token and check payload (requires JWT secret)
    # from app.core.security import decode_token
    # payload = decode_token(token_data["access_token"])
    # assert payload is not None
    # assert payload.get("user_id") == user_in_db.id
    # assert payload.get("role") == admin_role.name


async def test_login_incorrect_password(async_client: AsyncClient, db_session: AsyncSession):
    test_username = "testuser_wrongpass"
    test_email = "testuser_wrongpass@example.com"
    # Create user
    user_in = UserCreate(username=test_username, email=test_email, password="correctpassword")
    await crud_user.create(db=db_session, obj_in=user_in)
    await db_session.commit()

    login_data = {
        "username": test_username,
        "password": "incorrectpassword"
    }
    response = await async_client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Incorrect username or password"

async def test_login_nonexistent_user(async_client: AsyncClient):
    login_data = {
        "username": "nonexistentuser",
        "password": "anypassword"
    }
    response = await async_client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED # Or based on how your auth handles it
    # The detail message might vary if user not found vs. wrong password for found user are distinguished
    # Current implementation returns "Incorrect username or password" for both.

async def test_get_users_me_unauthenticated(async_client: AsyncClient):
    response = await async_client.get(f"{settings.API_V1_STR}/users/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Not authenticated" # Default from OAuth2PasswordBearer

async def test_get_users_me_authenticated(async_client: AsyncClient, db_session: AsyncSession):
    # 1. Create user and role, then login to get a token
    test_username = "test_me_user"
    test_email = "test_me_user@example.com"
    test_password = "password123"

    user_role = await crud_role.get_by_name(db=db_session, name="User")
    if not user_role:
        user_role = await crud_role.create(db=db_session, name="User", description="Test User role")

    user_obj = UserCreate(username=test_username, email=test_email, password=test_password)
    created_user = await crud_user.create(db=db_session, obj_in=user_obj)
    await crud_user.assign_role_to_user(db=db_session, user=created_user, role=user_role)
    await db_session.commit()

    login_resp = await async_client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": test_username, "password": test_password}
    )
    assert login_resp.status_code == status.HTTP_200_OK
    token = login_resp.json()["access_token"]

    # 2. Access /users/me with the token
    headers = {"Authorization": f"Bearer {token}"}
    response = await async_client.get(f"{settings.API_V1_STR}/users/me", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    user_data = response.json()
    assert user_data["username"] == test_username
    assert user_data["email"] == test_email
    assert user_data["id"] == created_user.id
    assert len(user_data["roles"]) == 1
    assert user_data["roles"][0]["name"] == "User"


async def test_admin_can_create_user(async_client: AsyncClient, db_session: AsyncSession):
    # 1. Create an admin user and log them in
    admin_username = "superadmin"
    admin_email = "superadmin@example.com"
    admin_password = "superadminpassword"

    admin_role = await crud_role.get_by_name(db=db_session, name="Admin")
    if not admin_role:
        admin_role = await crud_role.create(db=db_session, name="Admin", description="Admin role")

    admin_user_in = UserCreate(username=admin_username, email=admin_email, password=admin_password)
    admin_user_db = await crud_user.create(db=db_session, obj_in=admin_user_in)
    await crud_user.assign_role_to_user(db=db_session, user=admin_user_db, role=admin_role)
    await db_session.commit()

    login_resp = await async_client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": admin_username, "password": admin_password}
    )
    assert login_resp.status_code == status.HTTP_200_OK
    admin_token = login_resp.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # 2. Admin creates a new user
    new_user_data = {
        "username": "newlycreateduser",
        "email": "newlycreated@example.com",
        "password": "newpassword123",
        "is_active": True
    }
    response = await async_client.post(f"{settings.API_V1_STR}/users/", json=new_user_data, headers=admin_headers)
    assert response.status_code == status.HTTP_201_CREATED
    created_user_info = response.json()
    assert created_user_info["username"] == "newlycreateduser"
    assert created_user_info["email"] == "newlycreated@example.com"
    assert "id" in created_user_info
    assert created_user_info["roles"] == [] # By default, create_user doesn't assign roles

    # Verify user in DB
    db_user = await crud_user.get_by_username(db=db_session, username="newlycreateduser")
    assert db_user is not None
    assert db_user.email == "newlycreated@example.com"


async def test_non_admin_cannot_create_user(async_client: AsyncClient, db_session: AsyncSession):
    # 1. Create a non-admin user and log them in
    non_admin_username = "regularuser"
    non_admin_email = "regularuser@example.com"
    non_admin_password = "regularpassword"

    user_role = await crud_role.get_by_name(db=db_session, name="User")
    if not user_role:
        user_role = await crud_role.create(db=db_session, name="User", description="User role")

    non_admin_user_in = UserCreate(username=non_admin_username, email=non_admin_email, password=non_admin_password)
    non_admin_user_db = await crud_user.create(db=db_session, obj_in=non_admin_user_in)
    await crud_user.assign_role_to_user(db=db_session, user=non_admin_user_db, role=user_role)
    await db_session.commit()

    login_resp = await async_client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": non_admin_username, "password": non_admin_password}
    )
    assert login_resp.status_code == status.HTTP_200_OK
    non_admin_token = login_resp.json()["access_token"]
    non_admin_headers = {"Authorization": f"Bearer {non_admin_token}"}

    # 2. Non-admin attempts to create a new user
    new_user_data = {
        "username": "anothernewuser",
        "email": "anothernew@example.com",
        "password": "password"
    }
    response = await async_client.post(f"{settings.API_V1_STR}/users/", json=new_user_data, headers=non_admin_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN # Forbidden
    assert "not authorized" in response.json()["detail"].lower()
