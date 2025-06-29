from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime, func
from sqlalchemy.orm import relationship

from ..db.database import Base
from .type import DeliveryState

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(DeliveryState), nullable=False)
    delivery_id = Column(Integer, ForeignKey('deliveries.id'), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    delivery = relationship("Delivery", back_populates="events")
    
    def to_dict(self):
        """
        Convert the Event instance to a dictionary.
        """
        return {
            "id": self.id,
            "type": self.type,
            "delivery_id": self.delivery_id
        }