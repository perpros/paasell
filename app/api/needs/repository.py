from sqlalchemy.orm import Session
from sqlalchemy import not_
from ... import models

def get_open_needs(db: Session):
    return db.query(models.Need).filter(
        not_(models.Need.offers.any(models.Offer.status == models.OfferStatus.accepted))
    ).all()
