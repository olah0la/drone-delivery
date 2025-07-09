from pydantic import BaseModel, Field, ConfigDict

from ..models import DeliveryState

class DeliverySchema(BaseModel):
    """Schema for Delivery model."""
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(None, description="Unique identifier for the delivery")
    name: str = Field(..., description="Name of the delivery") # should have a unique constraint and a fixed length
    status: DeliveryState = Field(..., description="Current status of the delivery")


class DeliveryCountSchema(BaseModel):
    """Schema for counting deliveries."""
    ongoing_deliveries: int = Field(..., ge=0, description="Count of ongoing deliveries")
    total_deliveries: int = Field(..., ge=0, description="Total count of deliveries") 
