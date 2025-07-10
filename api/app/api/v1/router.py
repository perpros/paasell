from fastapi import APIRouter

# Placeholder for importing endpoint routers
from app.auth.router import router as auth_router
from app.users.router import router as users_router

api_router = APIRouter()

# Include your endpoint routers here
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
