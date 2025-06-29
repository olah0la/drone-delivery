from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas import EventSchema
from ..services import ingest_event, count_deliveries, get_delivery_events, get_ongoing_deliveries
from ..db.database import get_db


router = APIRouter()

@router.get("/deliveries")
async def ongoing_deliveries(db: AsyncSession = Depends(get_db)) -> List[dict]:
    deliveries = await get_ongoing_deliveries(db)
    return deliveries

@router.post("/deliveries/{id}/events")
async def create_event(id: str, event: EventSchema, db: AsyncSession = Depends(get_db)):
    try:
        async with db.begin():
            ingested_event = await ingest_event(db, id, event)
            return ingested_event
    except HTTPException as e:
        raise e

@router.get("/deliveries/{id}/events")
async def get_events(id: str, db: AsyncSession = Depends(get_db)):
    delivery_events = await get_delivery_events(db, id)
    if not delivery_events:
        raise HTTPException(status_code=404, detail="No events found for this delivery.")
    return delivery_events

@router.get("/counts")
async def total_ongoing_deliveries(db: AsyncSession = Depends(get_db)):
    """Get the total number of ongoing deliveries and total deliveries since the beginning."""
    ongoing_delivery_count = await count_deliveries(db)
    return ongoing_delivery_count
