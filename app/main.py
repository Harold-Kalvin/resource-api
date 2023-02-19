from fastapi import Depends, FastAPI

from .auth.router import current_active_user
from .auth.router import router as auth_router
from .resource.router import router as resource_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(resource_router, dependencies=[Depends(current_active_user)])
