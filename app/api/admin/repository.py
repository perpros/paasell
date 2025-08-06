from sqlalchemy.orm import Session
from ... import models
from ...schemas import need as need_schema

def create_need(db: Session, need: need_schema.NeedCreate, creator_id: int):
    db_need = models.Need(
        **need.dict(),
        created_by=creator_id
    )
    db.add(db_need)
    db.commit()
    db.refresh(db_need)
    return db_need
