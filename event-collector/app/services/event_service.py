from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..schemas import EventSchema, EventOutputSchema
from ..models import Delivery, Event
from .delivery_service import handle_delivery_event
from ..api.crud import create_event

async def ingest_event(db: AsyncSession, id: str, event: EventSchema) -> EventOutputSchema:
    """
    Ingest an event for a delivery. If the delivery does not exist, create it.
    If the delivery exists, update its status and create a new event.
    """
    delivery = await handle_delivery_event(db, event.type, id)
    new_event = await create_event(db, delivery.name, event.type)
    return EventOutputSchema.from_orm(new_event)

async def get_delivery_events(db: AsyncSession, id: str) -> List[EventOutputSchema]:
    """
    Retrieve all events for a specific delivery.
    """
    delivery_query = select(Delivery).filter(Delivery.name == id)
    result = await db.execute(delivery_query)
    delivery = result.scalars().first()
    if not delivery:
        return []
    events_query = select(Event).filter(Event.delivery_id == delivery.id)
    result = await db.execute(events_query)
    events = result.scalars().all()
    return [EventOutputSchema.from_orm(event) for event in events]