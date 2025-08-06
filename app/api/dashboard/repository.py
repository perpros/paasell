from sqlalchemy.orm import Session
from ... import models

def get_distributor_orders(db: Session, distributor_id: int):
    return db.query(models.Order).join(models.DistributorCampaign).filter(
        models.DistributorCampaign.distributor_id == distributor_id
    ).all()

def get_distributor_transactions(db: Session, distributor_id: int):
    return db.query(models.TransactionLog).filter(
        models.TransactionLog.distributor_id == distributor_id
    ).all()
