from fastapi import FastAPI

from .api import router

app = FastAPI(title="Event Collector API")

app.include_router(router)
