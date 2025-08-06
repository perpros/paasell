from sqlalchemy.orm import Session
from ... import models
from ...schemas import distributor_campaign as distributor_campaign_schema

def create_distributor_campaign(db: Session, distributor_campaign: distributor_campaign_schema.DistributorCampaignCreate):
    db_distributor_campaign = models.DistributorCampaign(**distributor_campaign.dict())
    db.add(db_distributor_campaign)
    db.commit()
    db.refresh(db_distributor_campaign)
    return db_distributor_campaign
