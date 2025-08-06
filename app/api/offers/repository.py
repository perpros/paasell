from sqlalchemy.orm import Session
from ... import models
from ...schemas import offer as offer_schema

def create_offer(db: Session, offer: offer_schema.OfferCreate, need_id: int, supplier_id: int):
    db_offer = models.Offer(
        **offer.dict(),
        need_id=need_id,
        supplier_id=supplier_id
    )
    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)
    return db_offer
