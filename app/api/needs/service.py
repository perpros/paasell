from sqlalchemy.orm import Session
from . import repository

def get_open_needs(db: Session):
    return repository.get_open_needs(db=db)
