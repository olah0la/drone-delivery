from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas import DeliverySchema, DeliveryCountSchema
from ..models import Delivery, DeliveryState
from ..api.crud import (
    count_deliveries_by_state,
    count_total_deliveries,
    read_delivery_by_name,
    update_delivery,
    handle_new_delivery,
    get_deliveries_by_state
)


ONGOING_STATES = (DeliveryState.TAKEN_OFF, DeliveryState.PARCEL_COLLECTED, DeliveryState.LANDED)

async def get_delivery_counts(db: AsyncSession) -> DeliveryCountSchema:
    """
    Count ongoing and total deliveries.
    Returns a DeliveryCountSchema with the counts of ongoing and total deliveries."""
    """"""
    ongoing_deliveries = await count_deliveries_by_state(db, ONGOING_STATES)
    total_deliveries = await count_total_deliveries(db)
    return DeliveryCountSchema(
        ongoing_deliveries=ongoing_deliveries,
        total_deliveries=total_deliveries
    )

async def get_ongoing_deliveries(db: AsyncSession) -> List[DeliverySchema]:
    """
    Retrieve all ongoing deliveries.
    Returns a list of DeliverySchema for ongoing deliveries.
    """
    deliveries = await get_deliveries_by_state(db, ONGOING_STATES)
    return [DeliverySchema.from_orm(delivery) for delivery in deliveries]

async def handle_delivery_event(db: AsyncSession, event_type: DeliveryState, delivery_name: str) -> Delivery:
    """
    Handle a delivery event by either creating a new delivery or updating an existing one.
    If the delivery does not exist, it will be created with the provided name and event type
    If it exists, its status will be updated to the provided event type.
    Returns the Delivery object.
    """
    delivery = await read_delivery_by_name(db, delivery_name)
    if not delivery:
        delivery = await handle_new_delivery(db, delivery_name, event_type)
    else:
        delivery = await update_delivery(db, delivery_name, event_type)
    return delivery
