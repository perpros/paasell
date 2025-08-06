from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ... import dependencies
from ...schemas import campaign as campaign_schema
from . import service

router = APIRouter()

@router.get("/active", response_model=List[campaign_schema.Campaign])
def read_active_campaigns(db: Session = Depends(dependencies.get_db)):
    """
    Retrieve active campaigns.
    """
    campaigns = service.get_active_campaigns(db=db)
    return campaigns
