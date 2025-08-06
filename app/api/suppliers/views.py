from fastapi import APIRouter, Depends
from ... import models, dependencies

router = APIRouter()

@router.get("/dashboard")
def supplier_dashboard(current_user: models.User = Depends(dependencies.role_checker([models.Role.supplier]))):
    return {"message": f"Welcome to the supplier dashboard, {current_user.username}!"}
