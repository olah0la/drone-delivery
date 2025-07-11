
from sqlalchemy import Column, Integer, String, Enum, DateTime, func, Index
from sqlalchemy.orm import relationship

from .type import DeliveryState
from ..db.database import Base

class Delivery(Base):
    __tablename__ = 'deliveries'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True, unique=True)
    status = Column(Enum(DeliveryState), nullable=False, default=DeliveryState.PARCEL_COLLECTED)
    created_at = Column(DateTime, server_default=func.now())

    events = relationship("Event", back_populates="delivery", cascade="all, delete-orphan")
        
    @property
    def is_ongoing(self):
        return self.status in DeliveryState.ongoing_states()

    def __repr__(self):
        return f"<Delivery(id={self.id}, name={self.name}, status={self.status}, created_at={self.created_at})>"