from pydantic import BaseModel
from datetime import datetime

class CampaignBase(BaseModel):
    name: str
    description: str | None = None
    start_date: datetime
    end_date: datetime

class CampaignCreate(CampaignBase):
    pass

class Campaign(CampaignBase):
    id: int
    created_by: int

    class Config:
        from_attributes = True
