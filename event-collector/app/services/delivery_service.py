from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas import DeliverySchema, DeliveryCountSchema
from ..models import Delivery, DeliveryState
from ..api.crud import (
    count_deliveries_by_state,
    count_total_deliveries,
    read_delivery,
    update_delivery,
    handle_new_delivery,
    get_deliveries_by_state
)


ONGOING_STATES = (DeliveryState.TAKEN_OFF, DeliveryState.PARCEL_COLLECTED, DeliveryState.LANDED)

async def count_deliveries(db: AsyncSession) -> DeliveryCountSchema:
    """Count the total number of ongoing and total deliveries."""
    ongoing_deliveries = await count_deliveries_by_state(db, ONGOING_STATES)
    total_deliveries = await count_total_deliveries(db)
    return DeliveryCountSchema(
        ongoing_deliveries=ongoing_deliveries,
        total_deliveries=total_deliveries
    )

async def get_ongoing_deliveries(db: AsyncSession) -> List[DeliverySchema]:
    """Retrieve all ongoing deliveries."""
    deliveries = await get_deliveries_by_state(db, ONGOING_STATES)
    if not deliveries:
        return []
    return [delivery.to_dict() for delivery in deliveries] 

async def handle_delivery_event(db: AsyncSession, event_type: DeliveryState, delivery_name: str) -> Delivery:
    """Handle a delivery event by updating the delivery status."""
    # FU: fix the id =/= name issue
    delivery = await read_delivery(db, delivery_name)
    if not delivery:
        delivery = await handle_new_delivery(db, delivery_name, event_type)
    else:
        delivery = await update_delivery(db, delivery_name, event_type)
    return delivery
