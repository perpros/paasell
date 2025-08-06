from sqlalchemy.orm import Session
import secrets
from . import repository
from ...schemas import distributor_campaign as distributor_campaign_schema

def activate_campaign_for_distributor(db: Session, campaign_id: int, distributor_id: int):
    # Generate a unique link
    unique_link = f"/portal/{campaign_id}/{secrets.token_hex(8)}"

    distributor_campaign_data = distributor_campaign_schema.DistributorCampaignCreate(
        campaign_id=campaign_id,
        distributor_id=distributor_id,
        unique_link=unique_link
    )
    return repository.create_distributor_campaign(db=db, distributor_campaign=distributor_campaign_data)
