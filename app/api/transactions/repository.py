from sqlalchemy.orm import Session
from ... import models
from ...schemas import transaction_log as transaction_log_schema

def create_transaction_log(db: Session, transaction_log: transaction_log_schema.TransactionLogCreate):
    db_transaction_log = models.TransactionLog(**transaction_log.dict())
    db.add(db_transaction_log)
    db.commit()
    db.refresh(db_transaction_log)
    return db_transaction_log

def get_all_transactions(db: Session):
    return db.query(models.TransactionLog).all()
