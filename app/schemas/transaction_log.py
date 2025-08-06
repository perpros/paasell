from pydantic import BaseModel
from datetime import datetime

class TransactionLogBase(BaseModel):
    order_id: int
    distributor_id: int
    commission_amount: float

class TransactionLogCreate(TransactionLogBase):
    pass

class TransactionLog(TransactionLogBase):
    id: int
    transaction_date: datetime

    class Config:
        from_attributes = True
