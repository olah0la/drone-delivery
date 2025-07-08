from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from ..schemas import EventSchema, EventOutputSchema
from ..models import Delivery, Event
from .delivery_service import handle_delivery_event
from ..api.crud import create_event


async def ingest_event(db: AsyncSession, delivery_name: str, event: EventSchema) -> EventOutputSchema:
    """
    Ingest an event for a delivery. If the delivery does not exist, create it.
    If the delivery exists, update its status and create a new event.
    Returns the created or updated event as EventOutputSchema.
    If the delivery does not exist, it will be created with the initial event type.
    If the delivery exists, it will be updated with the new event type.
    """
    delivery = await handle_delivery_event(db, event.type, delivery_name)
    new_event = await create_event(db, delivery.name, event.type)
    return EventOutputSchema.from_orm(new_event)

async def get_delivery_events(db: AsyncSession, delivery_name: str) -> Optional[List[EventOutputSchema]]:
    """
    Get all events for a specific delivery by its name.
    Returns a list of EventOutputSchema or None if the delivery does not exist.
    If the delivery exists but has no events, returns an empty list.
    """
    delivery_query = (
        select(Delivery)
        .options(joinedload(Delivery.events))
        .filter(Delivery.name == delivery_name)
    )
    result = await db.execute(delivery_query)
    delivery = result.scalars().first()
    if not delivery:
        return None
    return [EventOutputSchema.from_orm(event) for event in delivery.events]
