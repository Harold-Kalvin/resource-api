from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.schemas import User, UserRegisterInput
from app.database.session import get_session

from .. import repository

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(user: UserRegisterInput, db: Session = Depends(get_session)):
    existing_user = repository.get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists")
    return repository.create_user(db, user)
