from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ... import dependencies, models
from ...schemas import need as need_schema, offer as offer_schema
from . import service as need_service
from ..offers import service as offer_service


router = APIRouter()

@router.get("/open", response_model=List[need_schema.Need])
def read_open_needs(db: Session = Depends(dependencies.get_db)):
    """
    Retrieve open market needs.
    """
    needs = need_service.get_open_needs(db=db)
    return needs

@router.post(
    "/{need_id}/offers",
    response_model=offer_schema.Offer
)
def create_offer_for_need(
    need_id: int,
    offer: offer_schema.OfferCreate,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.role_checker([models.Role.supplier]))
):
    """
    Create an offer for a specific need.
    """
    supplier_id = current_user.id
    # We should probably check if the need exists and is open.
    # I will add this logic later if needed.
    new_offer = offer_service.create_offer(
        db=db, offer=offer, need_id=need_id, supplier_id=supplier_id
    )
    return new_offer
