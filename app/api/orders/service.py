from sqlalchemy.orm import Session
from . import repository as order_repository
from ..transactions import repository as transaction_repository
from ...schemas import order as order_schema, transaction_log as transaction_log_schema
from ... import models

COMMISSION_RATE = 0.10

def create_order(db: Session, order: order_schema.OrderCreate):
    # 1. Create the order
    db_order = order_repository.create_order(db=db, order=order)

    # 2. Get the distributor ID from the distributor campaign
    distributor_campaign = db.query(models.DistributorCampaign).filter(
        models.DistributorCampaign.id == order.distributor_campaign_id
    ).first()
    if not distributor_campaign:
        # This should ideally not happen if the frontend is correct
        return db_order

    distributor_id = distributor_campaign.distributor_id

    # 3. Calculate commission
    commission_amount = order.amount * COMMISSION_RATE

    # 4. Create transaction log
    transaction_log_data = transaction_log_schema.TransactionLogCreate(
        order_id=db_order.id,
        distributor_id=distributor_id,
        commission_amount=commission_amount
    )
    transaction_repository.create_transaction_log(db=db, transaction_log=transaction_log_data)

    return db_order
