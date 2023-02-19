from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_session
from app.resource.codes import ErrorCode

from . import repository
from .schemas import Resource, ResourceFilters, ResourceInput

router = APIRouter(prefix="/resources", tags=["resources"])


@router.post("/", response_model=Resource, status_code=status.HTTP_201_CREATED)
async def create_resource(resource: ResourceInput, db: Session = Depends(get_session)):
    existing_resource = await repository.get_resource_by_name(db, name=resource.name)
    if existing_resource:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=ErrorCode.RESOURCE_ALREADY_EXISTS)
    return await repository.create_resource(db=db, resource=resource)


@router.get("/", response_model=list[Resource])
async def read_resources(filters: ResourceFilters = Depends(), db: Session = Depends(get_session)):
    resources = await repository.get_resources(db, filters)
    return resources


@router.get("/{resource_id}", response_model=Resource)
async def read_resource(resource_id: int, db: Session = Depends(get_session)):
    resource = await repository.get_resource(db, resource_id=resource_id)
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.RESOURCE_NOT_FOUND)
    return resource


@router.patch("/{resource_id}", response_model=Resource)
async def update_resource(resource_id: int, resource: ResourceInput, db: Session = Depends(get_session)):
    existing_resource = await repository.get_resource(db, resource_id=resource_id)
    if not existing_resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.RESOURCE_NOT_FOUND)

    await repository.update_resource(db, resource_id=resource_id, resource=resource)
    await db.refresh(existing_resource)
    return existing_resource


@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resource(resource_id: int, db: Session = Depends(get_session)):
    resource = await repository.get_resource(db, resource_id=resource_id)
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.RESOURCE_NOT_FOUND)

    await repository.delete_resource(db=db, resource_id=resource_id)
