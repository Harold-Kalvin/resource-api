from datetime import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.resource.codes import ErrorCode
from app.resource.repository import create_resource, get_resource
from app.resource.schemas import ResourceInput


@pytest.mark.asyncio
async def test_create_resource(authenticated_client: tuple[AsyncClient, AsyncSession]):
    client = authenticated_client[0]

    response = await client.post("/resources/", json={"name": "resource 569"})

    assert response.status_code == 201
    assert response.json()["name"] == "resource 569"


@pytest.mark.asyncio
async def test_resource_already_exists_on_create(authenticated_client: tuple[AsyncClient, AsyncSession]):
    client, session = authenticated_client
    await create_resource(session, ResourceInput(name="resource 462"))

    response = await client.post("/resources/", json={"name": "resource 462"})

    assert response.status_code == 409
    assert response.json()["detail"] == ErrorCode.RESOURCE_ALREADY_EXISTS


@pytest.mark.asyncio
async def test_read_resource(authenticated_client: tuple[AsyncClient, AsyncSession]):
    client, session = authenticated_client
    resource = await create_resource(session, ResourceInput(name="resource 125"))

    response = await client.get(f"/resources/{resource.id}/")

    assert response.status_code == 200
    assert response.json()["name"] == "resource 125"


@pytest.mark.asyncio
async def test_resource_not_found_on_read(authenticated_client: tuple[AsyncClient, AsyncSession]):
    client = authenticated_client[0]

    response = await client.get("/resources/1/")

    assert response.status_code == 404
    assert response.json()["detail"] == ErrorCode.RESOURCE_NOT_FOUND


@pytest.mark.asyncio
async def test_read_resources(authenticated_client: tuple[AsyncClient, AsyncSession]):
    client, session = authenticated_client
    await create_resource(session, ResourceInput(name="resource 684"))
    await create_resource(session, ResourceInput(name="resource 254"))

    response = await client.get("/resources/")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "resource 684"
    assert response.json()[1]["name"] == "resource 254"


@pytest.mark.asyncio
async def test_read_resources_with_date_filters(authenticated_client: tuple[AsyncClient, AsyncSession]):
    client, session = authenticated_client
    await create_resource(session, ResourceInput(name="resource 684"))
    resource_2 = await create_resource(session, ResourceInput(name="resource 254"))
    resource_2.created_at = datetime(1990, 1, 1, 10, 30)
    await session.commit()

    response = await client.get(
        "/resources/", params={"created_at_gte": "1990-01-01T10:30:00", "created_at_lte": "1991-01-01T10:30:00"}
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "resource 254"


@pytest.mark.asyncio
async def test_update_resource(authenticated_client: tuple[AsyncClient, AsyncSession]):
    client, session = authenticated_client
    resource = await create_resource(session, ResourceInput(name="resource 465"))

    # assert original name
    assert resource.name == "resource 465"

    response = await client.patch(f"/resources/{resource.id}/", json={"name": "new name"})

    # assert response returns the new name
    assert response.status_code == 200
    assert response.json()["name"] == "new name"

    # assert the object was actually updated
    await session.refresh(resource)
    assert resource.name == "new name"


@pytest.mark.asyncio
async def test_resource_not_found_on_update(authenticated_client: tuple[AsyncClient, AsyncSession]):
    client = authenticated_client[0]

    response = await client.patch("/resources/1/", json={"name": "new name"})

    assert response.status_code == 404
    assert response.json()["detail"] == ErrorCode.RESOURCE_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_resource(authenticated_client: tuple[AsyncClient, AsyncSession]):
    client, session = authenticated_client
    resource = await create_resource(session, ResourceInput(name="resource 812"))
    resource_id = resource.id

    response = await client.delete(f"/resources/{resource_id}/")

    # assert no content returned
    assert response.status_code == 204
    assert not response.content

    # assert the object was actually deleted
    assert not await get_resource(session, resource_id)


@pytest.mark.asyncio
async def test_resource_not_found_on_delete(authenticated_client: tuple[AsyncClient, AsyncSession]):
    client = authenticated_client[0]

    response = await client.delete("/resources/1/")

    assert response.status_code == 404
    assert response.json()["detail"] == ErrorCode.RESOURCE_NOT_FOUND
