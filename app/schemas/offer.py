from pydantic import BaseModel
from ..models import OfferStatus

class OfferBase(BaseModel):
    price: float

class OfferCreate(OfferBase):
    pass

class Offer(OfferBase):
    id: int
    need_id: int
    supplier_id: int
    status: OfferStatus

    class Config:
        from_attributes = True
