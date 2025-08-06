from sqlalchemy.orm import Session
from . import repository

def get_all_transactions(db: Session):
    return repository.get_all_transactions(db=db)
