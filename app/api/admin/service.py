from sqlalchemy.orm import Session
from . import repository
from ...schemas import need as need_schema

def create_need(db: Session, need: need_schema.NeedCreate, creator_id: int):
    return repository.create_need(db=db, need=need, creator_id=creator_id)
