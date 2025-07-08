from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas import EventSchema, DeliverySchema, EventOutputSchema
from ..services import count_deliveries, get_delivery_events, get_ongoing_deliveries
from ..db.database import get_db
from ..event_queue import process_event

router = APIRouter()

@router.get("/deliveries")
async def ongoing_deliveries(db: AsyncSession = Depends(get_db)) -> List[DeliverySchema]:
    """Get all ongoing deliveries."""
    try:
        deliveries = await get_ongoing_deliveries(db)
        return deliveries
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching ongoing deliveries: {str(e)}")

@router.post("/deliveries/{id}/events")
async def create_event(id: str, event: EventSchema, db: AsyncSession = Depends(get_db)) -> EventOutputSchema:
    """Ingest an event for a delivery. If the delivery does not exist, create it.
    If the delivery exists, update its status and create a new event."""
    try:
        async with db.begin():
            ingested_event = await process_event(id, event, db)
            return ingested_event
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing event: {str(e)}")

@router.get("/deliveries/{id}/events")
async def get_events(id: str, db: AsyncSession = Depends(get_db)) -> List[EventOutputSchema]:
    """Get all events for a specific delivery by its ID."""
    delivery_events = await get_delivery_events(db, id)
    if not delivery_events:
        raise HTTPException(status_code=404, detail="No events found for this delivery.")
    return delivery_events

@router.get("/deliveries/counts")
async def count_ongoing_deliveries(db: AsyncSession = Depends(get_db)) -> DeliverySchema:
    """Get the total number of ongoing deliveries and total deliveries since the beginning."""
    try:
        ongoing_delivery_count = await count_deliveries(db)
        return ongoing_delivery_count
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error counting deliveries: {str(e)}")
