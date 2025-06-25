from fastapi import FastAPI
from pydantic import BaseModel

class Event(BaseModel):
    type: str

app = FastAPI()


@app.post("/deliveries/{id}/events")
async def root(id: str, event: Event):
    print(f'Delivery {id} transitioned to {event.type}')
    return {"message": "ok"}
