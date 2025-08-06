from sqlalchemy.orm import Session
from . import repository
from ...schemas import offer as offer_schema

def create_offer(db: Session, offer: offer_schema.OfferCreate, need_id: int, supplier_id: int):
    return repository.create_offer(db=db, offer=offer, need_id=need_id, supplier_id=supplier_id)
