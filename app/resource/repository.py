from sqlalchemy import and_, delete, update
from sqlalchemy.orm import Session

from .models import Resource as ResourceORM
from .schemas import ResourceFilters, ResourceInput


def get_resource(db: Session, resource_id: int) -> ResourceORM:
    return db.query(ResourceORM).filter(ResourceORM.id == resource_id).first()


def get_resource_by_name(db: Session, name: str) -> ResourceORM:
    return db.query(ResourceORM).filter(ResourceORM.name == name).first()


def get_resources(db: Session, filters: ResourceFilters) -> list[ResourceORM]:
    filter_list = []
    if filters.created_at_gte:
        filter_list.append(ResourceORM.created_at >= filters.created_at_gte)
    if filters.created_at_lte:
        filter_list.append(ResourceORM.created_at <= filters.created_at_lte)
    return db.query(ResourceORM).filter(and_(*filter_list)).all()


def create_resource(db: Session, resource: ResourceInput) -> ResourceORM:
    db_resource = ResourceORM(**resource.dict())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource


def update_resource(db: Session, resource_id: int, resource: ResourceInput):
    statement = update(ResourceORM).where(ResourceORM.id == resource_id).values(**resource.dict())
    db.execute(statement)
    db.commit()


def delete_resource(db: Session, resource_id: int):
    statement = delete(ResourceORM).where(ResourceORM.id == resource_id)
    db.execute(statement)
    db.commit()
