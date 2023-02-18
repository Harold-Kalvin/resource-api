from sqlalchemy.orm import Session

from app.auth.hashing import get_password_hash
from app.auth.models import User as UserORM
from app.auth.schemas import UserRegisterInput


def create_user(db: Session, user: UserRegisterInput) -> UserORM:
    db_user = UserORM(email=user.email, password=get_password_hash(user.password), username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str) -> UserORM:
    return db.query(UserORM).filter(UserORM.email == email).first()
