from pydantic import BaseModel

class NeedBase(BaseModel):
    title: str
    description: str | None = None

class NeedCreate(NeedBase):
    pass

class Need(NeedBase):
    id: int
    created_by: int

    class Config:
        from_attributes = True
