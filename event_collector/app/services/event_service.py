from ..schemas.event import EventSchema

def ingest_event(id: str, event: EventSchema) -> dict:
    """
    
    """
    print(f'Delivery {id} transitioned to {event.type}')
    return {"message": "ok"}
