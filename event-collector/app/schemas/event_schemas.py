from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class EventType(str, Enum):
    PARCEL_COLLECTED = "PARCEL_COLLECTED"
    TAKEN_OFF = "TAKEN_OFF"
    LANDED = "LANDED"
    CRASHED = "CRASHED"
    PARCEL_DELIVERED = "PARCEL_DELIVERED"

class EventSchema(BaseModel):
    type: EventType = Field(..., description="Type of the event")
    created_at: datetime = Field(None, description="Timestamp of when the event was created")

class EventOutputSchema(BaseModel):
    """Schema for outputting event details."""
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(None, description="Unique identifier for the event")
    type: EventType = Field(..., description="Type of the event")
    delivery_id: int = Field(..., description="ID of the delivery associated with the event")
    created_at: datetime = Field(..., description="Timestamp of when the event was created")

