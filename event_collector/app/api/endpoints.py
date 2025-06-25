from fastapi import APIRouter

from ..schemas import EventSchema
from ..services import ingest_event

router = APIRouter()

@router.get("/deliveries")
async def get_ongoing_deliveries():
    print('Getting ongoing deliveries')
    return {"deliveries": []}

@router.post("/deliveries/{id}/events")
async def create_event(id: str, event: EventSchema):
    print(f'Delivery {id} transitioned to {event.type}')
    return ingest_event(id, event)

@router.get("/deliveries/{id}/events")
async def get_events(id: str):
    print(f'Getting events for delivery {id}')
    return {"events": []}

@router.get("/counts")
async def total_ongoing_deliveries():
    print('Getting total ongoing deliveries')
    return {"ongoing_deliveries": 0, "total_deliveries": 0}
