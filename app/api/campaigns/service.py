from sqlalchemy.orm import Session
from . import repository

def get_active_campaigns(db: Session):
    return repository.get_active_campaigns(db=db)
