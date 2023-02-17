from fastapi import FastAPI

from app.database.session import engine
from app.resource.routes import router as resource_router

from .resource import models

models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(resource_router)
