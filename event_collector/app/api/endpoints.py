from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas import EventSchema
from ..services import ingest_event, count_deliveries, get_delivery_events, get_ongoing_deliveries
from ..db.database import get_db


router = APIRouter()

@router.get("/deliveries")
async def ongoing_deliveries(db: AsyncSession = Depends(get_db)):
    ongoing_deliveries = await get_ongoing_deliveries(db)
    return ongoing_deliveries

@router.post("/deliveries/{id}/events")
async def create_event(id: str, event: EventSchema, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        ingested_events = await ingest_event(db, id, event)
        return ingested_events

@router.get("/deliveries/{id}/events")
async def get_events(id: str, db: AsyncSession = Depends(get_db)):
    delivery_events = await get_delivery_events(db, id)
    if not delivery_events:
        return {"message": "No events found for this delivery."}
    return delivery_events

@router.get("/counts")
async def total_ongoing_deliveries(db: AsyncSession = Depends(get_db)):
    """Get the total number of ongoing deliveries and total deliveries since the beginning."""
    total_ongoing_deliveries = await count_deliveries(db)
    return total_ongoing_deliveries
