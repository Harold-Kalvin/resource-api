import uuid

from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from app.auth.dependencies import get_user_manager
from app.auth.models import User
from app.auth.schemas import UserCreate, UserRead

from .backend import auth_backend

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)

router = APIRouter(prefix="/auth", tags=["auth"])

# login, logout routes
router.include_router(fastapi_users.get_auth_router(auth_backend))

# register route
router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))
