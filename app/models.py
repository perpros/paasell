import enum
from sqlalchemy import Boolean, Column, Integer, String, Enum
from .database import Base

class Role(enum.Enum):
    admin = "admin"
    distributor = "distributor"
    supplier = "supplier"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(Role))
