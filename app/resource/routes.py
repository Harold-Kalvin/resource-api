from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_session

from . import repository
from .schemas import Resource, ResourceFilters, ResourceInput

router = APIRouter(prefix="/resources", tags=["resources"])


@router.post("/", response_model=Resource, status_code=status.HTTP_201_CREATED)
def create_resource(resource: ResourceInput, db: Session = Depends(get_session)):
    existing_resource = repository.get_resource_by_name(db, name=resource.name)
    if existing_resource:
        raise HTTPException(status_code=409, detail="Resource with this name already exists")
    return repository.create_resource(db=db, resource=resource)


@router.get("/", response_model=list[Resource])
def read_resources(filters: ResourceFilters = Depends(), db: Session = Depends(get_session)):
    resources = repository.get_resources(db, filters)
    return resources


@router.get("/{resource_id}", response_model=Resource)
def read_resource(resource_id: int, db: Session = Depends(get_session)):
    resource = repository.get_resource(db, resource_id=resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource


@router.patch("/{resource_id}", response_model=Resource)
def update_resource(resource_id: int, resource: ResourceInput, db: Session = Depends(get_session)):
    existing_resource = repository.get_resource(db, resource_id=resource_id)
    if not existing_resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    repository.update_resource(db, resource_id=resource_id, resource=resource)
    db.refresh(existing_resource)
    return existing_resource


@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource(resource_id: int, db: Session = Depends(get_session)):
    resource = repository.get_resource(db, resource_id=resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    repository.delete_resource(db=db, resource_id=resource_id)
