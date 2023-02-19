import uuid

from fastapi_users import BaseUserManager, UUIDIDMixin

from .models import User


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    pass
