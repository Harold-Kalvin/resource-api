from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.database import Base


class Resource(Base):
    __tablename__ = "resource"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now())
