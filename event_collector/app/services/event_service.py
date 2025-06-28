from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..schemas.event import EventSchema
from ..models import Delivery, Event
from .delivery_service import handle_delivery_event
from ..api.crud import create_event

async def ingest_event(db: AsyncSession, id: str, event: EventSchema) -> dict:
    """
    Ingest an event for a delivery. If the delivery does not exist, create it.
    If the delivery exists, update its status and create a new event.
    """
    delivery = await handle_delivery_event(db, event.type, id)
    new_event = await create_event(db, delivery.name, event.type)
    return {
        "delivery": delivery.to_dict(),
        "event": new_event.to_dict()
    }

async def get_delivery_events(db: AsyncSession, id: str) -> list:
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
    return [event.to_dict() for event in events]
