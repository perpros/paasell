from sqlalchemy.orm import Session
from ... import models
from ...schemas import order as order_schema

def create_order(db: Session, order: order_schema.OrderCreate):
    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order
