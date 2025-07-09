from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime, func
from sqlalchemy.orm import relationship

from ..db.database import Base
from .type import DeliveryState

class Event(Base):
    __tablename__ = 'events'

    id: int = Column(Integer, primary_key=True, index=True)
    type: DeliveryState = Column(Enum(DeliveryState), nullable=False)
    delivery_id: int = Column(Integer, ForeignKey('deliveries.id'), nullable=False) # ondelete cascade ?
    created_at: datetime = Column(DateTime, server_default=func.now(), nullable=False)
    
    delivery = relationship("Delivery", back_populates="events")

    def __repr__(self):
        return f"<Event(id={self.id}, type={self.type}, delivery_id={self.delivery_id}, created_at={self.created_at})>"
    