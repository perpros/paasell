from sqlalchemy.orm import Session
from ... import models
from datetime import datetime

def get_active_campaigns(db: Session):
    now = datetime.utcnow()
    return db.query(models.Campaign).filter(
        models.Campaign.start_date <= now,
        models.Campaign.end_date >= now
    ).all()
