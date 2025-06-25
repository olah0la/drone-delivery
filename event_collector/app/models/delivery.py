
from sqlalchemy import Column, Integer, String
from sqlalchemy import Enum

from .type import State
from ..db.database import Base

class Delivery(Base):
    __tablename__ = 'deliveries'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    status = Column(Enum(State), nullable=False, default=State.PARCEL_COLLECTED)
