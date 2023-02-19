from sqlalchemy import and_, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Resource as ResourceORM
from .schemas import ResourceFilters, ResourceInput


async def get_resource(db: AsyncSession, resource_id: int) -> ResourceORM | None:
    statement = select(ResourceORM).where(ResourceORM.id == resource_id)
    return (await db.execute(statement)).scalar()


async def get_resource_by_name(db: AsyncSession, name: str) -> ResourceORM | None:
    statement = select(ResourceORM).where(ResourceORM.name == name)
    return (await db.execute(statement)).scalar()


async def get_resources(db: AsyncSession, filters: ResourceFilters) -> list[ResourceORM]:
    filter_list = []
    if filters.created_at_gte:
        filter_list.append(ResourceORM.created_at >= filters.created_at_gte)
    if filters.created_at_lte:
        filter_list.append(ResourceORM.created_at <= filters.created_at_lte)

    statement = select(ResourceORM).where(and_(*filter_list))
    return (await db.execute(statement)).scalars().all()


async def create_resource(db: AsyncSession, resource: ResourceInput) -> ResourceORM:
    db_resource = ResourceORM(**resource.dict())
    db.add(db_resource)
    await db.commit()
    await db.refresh(db_resource)
    return db_resource


async def update_resource(db: AsyncSession, resource_id: int, resource: ResourceInput):
    statement = update(ResourceORM).where(ResourceORM.id == resource_id).values(**resource.dict())
    await db.execute(statement)
    await db.commit()


async def delete_resource(db: AsyncSession, resource_id: int):
    statement = delete(ResourceORM).where(ResourceORM.id == resource_id)
    await db.execute(statement)
    await db.commit()
