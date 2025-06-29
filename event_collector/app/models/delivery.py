
from sqlalchemy import Column, Integer, String, Enum, DateTime, func
from sqlalchemy.orm import relationship

from .type import State
from ..db.database import Base

class Delivery(Base):
    __tablename__ = 'deliveries'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    status = Column(Enum(State), nullable=False, default=State.PARCEL_COLLECTED)
    created_at = Column(DateTime, server_default=func.now())

    events = relationship("Event", back_populates="delivery", cascade="all, delete-orphan")

    def __init__(self, name: str, status: State = State.PARCEL_COLLECTED):
        self.name = name
        self.status = status
        
    @property
    def is_ongoing(self):
        return self.status in (State.TAKEN_OFF, State.PARCEL_COLLECTED, State.LANDED)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status
        }