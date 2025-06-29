from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from ..models import Delivery, Event, DeliveryState
from ..core import settings


async def create_delivery(db: AsyncSession, delivery_name: str, event_type: DeliveryState) -> Delivery:
    """Create a new delivery and handle the event."""
    delivery = Delivery(name=delivery_name, status=event_type)
    db.add(delivery)
    await db.commit()
    await db.refresh(delivery)
    return delivery

async def get_deliveries(db: AsyncSession) -> List[Delivery]:
    """Retrieve all deliveries from the database."""
    deliveries = await db.query(Delivery).all()
    return deliveries

async def get_deliveries_by_state(db: AsyncSession, states: List[DeliveryState]) -> List[Delivery]:
    """Retrieve deliveries filtered by their status."""
    query = select(Delivery).where(Delivery.status.in_(states))
    result = await db.execute(query)
    deliveries = result.scalars().all()
    return deliveries

async def read_delivery(db: AsyncSession, delivery_name: str) -> Delivery:
    """Retrieve a delivery by its name."""
    query = select(Delivery).where(Delivery.name == delivery_name)
    result = await db.execute(query)
    delivery = result.scalars().first()
    return delivery

async def update_delivery(db: AsyncSession, delivery_name: str, event_type: DeliveryState = DeliveryState.PARCEL_COLLECTED) -> Delivery:
    """Update the status of an existing delivery."""
    query = select(Delivery).where(Delivery.name == delivery_name)
    result = await db.execute(query)
    delivery = result.scalars().first()
    if not delivery:
        raise ValueError(f"Delivery with name {delivery_name} does not exist.")
    delivery.status = event_type
    return delivery

async def delete_delivery(db: AsyncSession, delivery_name: str) -> None:
    """Delete a delivery from the database."""
    query = select(Delivery).where(Delivery.name == delivery_name)
    result = await db.execute(query)
    delivery = result.scalars().first()
    if not delivery:
        raise ValueError(f"Delivery with name {delivery_name} does not exist.")
    await db.delete(delivery)
    await db.commit()

async def count_deliveries_by_state(db: AsyncSession, states: List[DeliveryState]) -> int:
    """Count the total number of ongoing and total deliveries."""
    query = select(func.count(Delivery.id)).where(Delivery.status.in_(states))
    result = await db.execute(query)
    count = result.scalar_one()
    return count

async def count_total_deliveries(db: AsyncSession) -> int:
    """Count the total number of deliveries."""
    query = select(func.count()).select_from(Delivery)
    result = await db.execute(query)
    count = result.scalar_one() 
    return count

async def handle_new_delivery(db: AsyncSession, delivery_name: str, event_type: DeliveryState) -> Delivery:
    """Handle a new delivery by creating it and ensuring the delivery history limit is respected."""
    total_deliveries = await count_total_deliveries(db)
    if total_deliveries >= settings.delivery_history_limit:
        print(f"Delivery history limit reached: {settings.delivery_history_limit}. Deleting oldest delivery.")
        oldest_delivery_query = select(Delivery).order_by(Delivery.created_at)
        result = await db.execute(oldest_delivery_query)
        oldest_delivery = result.scalars().first()
        if oldest_delivery:
            await db.delete(oldest_delivery)
    delivery = Delivery(name=delivery_name, status=event_type)
    db.add(delivery)
    return delivery

async def create_event(db: AsyncSession, delivery_name: str, event_type: DeliveryState) -> Event:
    """Create a new event for a delivery."""
    delivery = await read_delivery(db, delivery_name)
    event = Event(delivery_id=delivery.id, type=event_type)
    db.add(event)
    await db.flush()  # Persist the event to the database
    await db.refresh(event)  # Refresh the event to populate fields like id and created_at
    return event

async def read_event(db: AsyncSession, event_id: int) -> Event:
    """Retrieve an event by its ID."""
    event = await db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise ValueError(f"Event with ID {event_id} does not exist.")
    return event

async def update_event(db: AsyncSession, event_id: int, event_type: DeliveryState) -> Event:
    """Update the type of an existing event."""
    event = await db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise ValueError(f"Event with ID {event_id} does not exist.")
    event.type = event_type
    await db.commit()
    await db.refresh(event)
    return event

async def delete_event(db: AsyncSession, event_id: int) -> None:
    """Delete an event from the database."""
    event = await db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise ValueError(f"Event with ID {event_id} does not exist.")
    await  db.delete(event)
    await db.commit()
