from fastapi import FastAPI

from .auth.routes.auth import router as auth_router
from .resource.routes import router as resource_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(resource_router)
