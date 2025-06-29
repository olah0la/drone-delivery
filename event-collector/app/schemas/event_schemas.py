from datetime import datetime

from pydantic import BaseModel

class EventSchema(BaseModel):
    type: str

class EventOutputSchema(BaseModel):
    id: int
    type: str
    delivery_id: int
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True
