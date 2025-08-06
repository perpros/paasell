from pydantic import BaseModel

class DistributorCampaignBase(BaseModel):
    distributor_id: int
    campaign_id: int
    unique_link: str

class DistributorCampaignCreate(DistributorCampaignBase):
    pass

class DistributorCampaign(DistributorCampaignBase):
    id: int

    class Config:
        from_attributes = True
