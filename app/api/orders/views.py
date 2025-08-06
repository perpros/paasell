from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ... import dependencies
from ...schemas import order as order_schema
from . import service

router = APIRouter()

@router.post("/", response_model=order_schema.Order)
def create_order(
    order: order_schema.OrderCreate,
    db: Session = Depends(dependencies.get_db)
):
    """
    Create a new order.
    """
    new_order = service.create_order(db=db, order=order)
    return new_order
