from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import Enum

from ..db.database import Base
from .type import State

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(State), nullable=False)
    delivery_id = Column(String, ForeignKey('deliveries.id'), nullable=False)
    