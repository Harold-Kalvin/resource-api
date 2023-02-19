from fastapi import FastAPI

from .resource.router import router as resource_router

app = FastAPI()
app.include_router(resource_router)
