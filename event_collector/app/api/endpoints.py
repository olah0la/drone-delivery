from ..schemas import EventSchema

from fastapi import APIRouter

router = APIRouter()

@router.post("/deliveries/{id}/events")
async def root(id: str, event: EventSchema):
    print(f'Delivery {id} transitioned to {event.type}')
    return {"message": "ok"}
