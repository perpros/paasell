from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ... import models, dependencies
from ...schemas import need as need_schema, transaction_log as transaction_log_schema
from . import service
from ..transactions import service as transaction_service

router = APIRouter()

@router.get("/dashboard")
def admin_dashboard(current_user: models.User = Depends(dependencies.role_checker([models.Role.admin]))):
    return {"message": f"Welcome to the admin dashboard, {current_user.username}!"}

@router.post(
    "/needs",
    response_model=need_schema.Need
)
def create_need(
    need: need_schema.NeedCreate,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.role_checker([models.Role.admin]))
):
    """
    Create a new need (Admin only).
    """
    creator_id = current_user.id
    new_need = service.create_need(
        db=db, need=need, creator_id=creator_id
    )
    return new_need

@router.get(
    "/transactions",
    response_model=List[transaction_log_schema.TransactionLog]
)
def read_transactions(
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.role_checker([models.Role.admin]))
):
    """
    Retrieve all transactions (Admin only).
    """
    transactions = transaction_service.get_all_transactions(db=db)
    return transactions
