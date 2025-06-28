from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..models import Delivery, State
from ..core import settings
from ..api.crud import (
    count_deliveries_by_state,
    count_total_deliveries,
    create_delivery,
    read_delivery,
    update_delivery,
    delete_delivery,
    get_deliveries,
    get_deliveries_by_state
)

async def count_deliveries(db: AsyncSession) -> dict:
    """Count the total number of ongoing and total deliveries."""
    ONGOING_STATES = (State.TAKEN_OFF, State.PARCEL_COLLECTED, State.LANDED)
    return {
        "ongoing_deliveries": await count_deliveries_by_state(db, ONGOING_STATES),
        "total_deliveries": await count_total_deliveries(db)
    }

async def get_ongoing_deliveries(db: AsyncSession) -> list:
    """Retrieve all ongoing deliveries."""
    ONGOING_STATES = (State.TAKEN_OFF, State.PARCEL_COLLECTED, State.LANDED)
    deliveries = await get_deliveries_by_state(db, ONGOING_STATES)
    if not deliveries:
        return []
    return [delivery.to_dict() for delivery in deliveries] 

async def handle_new_delivery(db: AsyncSession, event_type: State, delivery_name: str) -> Delivery:
    """Handle a new delivery by creating it and ensuring the delivery history limit is respected."""
    total_deliveries = await count_total_deliveries(db)
    if total_deliveries >= settings.delivery_history_limit:
        print(f"Delivery history limit reached: {settings.delivery_history_limit}. Deleting oldest delivery.")
        oldest_delivery_query = select(Delivery).order_by(Delivery.created_at)
        result = await db.execute(oldest_delivery_query)
        oldest_delivery = result.scalars().first()
        if oldest_delivery: await delete_delivery(db, oldest_delivery.name)
    delivery = await create_delivery(db, delivery_name, event_type)        
    return delivery

async def handle_delivery_event(db: AsyncSession, event_type: State, delivery_name: str) -> Delivery:
    """Handle a delivery event by updating the delivery status."""
    # FU: fix the id =/= name issue
    delivery = await read_delivery(db, delivery_name)
    if not delivery:
        delivery = await handle_new_delivery(db, event_type, delivery_name)
    else:
        delivery = await update_delivery(db, delivery_name, event_type)
    return delivery
