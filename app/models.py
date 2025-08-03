import enum
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    Enum,
    ForeignKey,
    DateTime,
    Float,
)
from sqlalchemy.orm import relationship
from .database import Base
import datetime


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

    campaigns = relationship("Campaign", back_populates="creator")
    distributor_campaigns = relationship("DistributorCampaign", back_populates="distributor")
    needs = relationship("Need", back_populates="creator")
    offers = relationship("Offer", back_populates="supplier")
    transactions = relationship("TransactionLog", back_populates="distributor")


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    start_date = Column(DateTime, default=datetime.datetime.utcnow)
    end_date = Column(DateTime)
    created_by = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", back_populates="campaigns")
    distributor_campaigns = relationship("DistributorCampaign", back_populates="campaign")


class DistributorCampaign(Base):
    __tablename__ = "distributor_campaigns"

    id = Column(Integer, primary_key=True, index=True)
    distributor_id = Column(Integer, ForeignKey("users.id"))
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    unique_link = Column(String, unique=True, index=True)

    distributor = relationship("User", back_populates="distributor_campaigns")
    campaign = relationship("Campaign", back_populates="distributor_campaigns")
    orders = relationship("Order", back_populates="distributor_campaign")


class Need(Base):
    __tablename__ = "needs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    created_by = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", back_populates="needs")
    offers = relationship("Offer", back_populates="need")


class OfferStatus(enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"


class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    need_id = Column(Integer, ForeignKey("needs.id"))
    supplier_id = Column(Integer, ForeignKey("users.id"))
    price = Column(Float)
    status = Column(Enum(OfferStatus), default=OfferStatus.pending)

    need = relationship("Need", back_populates="offers")
    supplier = relationship("User", back_populates="offers")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    distributor_campaign_id = Column(Integer, ForeignKey("distributor_campaigns.id"))
    buyer_name = Column(String)
    buyer_email = Column(String)
    amount = Column(Float)
    order_date = Column(DateTime, default=datetime.datetime.utcnow)

    distributor_campaign = relationship("DistributorCampaign", back_populates="orders")
    transaction_log = relationship("TransactionLog", back_populates="order", uselist=False)


class TransactionLog(Base):
    __tablename__ = "transaction_log"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    distributor_id = Column(Integer, ForeignKey("users.id"))
    commission_amount = Column(Float)
    transaction_date = Column(DateTime, default=datetime.datetime.utcnow)

    order = relationship("Order", back_populates="transaction_log")
    distributor = relationship("User", back_populates="transactions")
