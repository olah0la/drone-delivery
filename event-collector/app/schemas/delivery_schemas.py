from pydantic import BaseModel, Field

from ..models import DeliveryState

class DeliverySchema(BaseModel):
    """Schema for Delivery model."""
    id: int = Field(None, description="Unique identifier for the delivery")
    name: str = Field(..., description="Name of the delivery")
    status: DeliveryState = Field(..., description="Current status of the delivery")

    class Config:
        orm_mode = True

class DeliveryCountSchema(BaseModel):
    """Schema for counting deliveries."""
    ongoing_deliveries: int = Field(..., description="Count of ongoing deliveries")
    total_deliveries: int = Field(..., description="Total count of deliveries") 
