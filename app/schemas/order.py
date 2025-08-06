from pydantic import BaseModel
from datetime import datetime

class OrderBase(BaseModel):
    distributor_campaign_id: int
    buyer_name: str
    buyer_email: str
    amount: float

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    order_date: datetime

    class Config:
        from_attributes = True
