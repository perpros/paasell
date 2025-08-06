from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ... import dependencies, models
from ...schemas import distributor_campaign as distributor_campaign_schema
from . import service

router = APIRouter()

@router.post(
    "/campaigns/{campaign_id}/activate",
    response_model=distributor_campaign_schema.DistributorCampaign,
)
def activate_campaign(
    campaign_id: int,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.role_checker([models.Role.distributor]))
):
    """
    Activate a campaign for the current distributor.
    """
    distributor_id = current_user.id
    # We should probably check if the campaign exists and is active
    # And if the distributor hasn't already activated this campaign
    # I will add this logic later if needed, for now, let's keep it simple.
    distributor_campaign = service.activate_campaign_for_distributor(
        db=db, campaign_id=campaign_id, distributor_id=distributor_id
    )
    return distributor_campaign
