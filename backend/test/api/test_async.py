import httpx
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager

from test_config import TEST_USER, TEST_PASSWORD
from main import app


@pytest_asyncio.fixture
async def life_app():
    async with LifespanManager(app) as manager:
        yield manager.app


@pytest_asyncio.fixture
async def client(life_app):
    async with httpx.AsyncClient(app=life_app, base_url="http://localhost") as client:
        yield client


@pytest.mark.asyncio
async def test_post_mongo(client):
    response = await client.post(
            "/mongo/",
            json={
                "_id": "test",
                "title": "test",
                "author": "test",
                "synopsis": "test"
            },
        )
    assert response.status_code == 201
    assert response.json() == {
        "_id": "test",
        "title": "test",
        "author": "test",
        "synopsis": "test"
    }


@pytest.mark.asyncio
async def test_post_mongo_ID_EXISTS_ERROR(client):
    response = await client.post(
            "/mongo/",
            json={
                "_id": "test",
                "title": "test",
                "author": "test",
                "synopsis": "test"
            },
        )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_mongo(client):
    response = await client.get("/mongo/")
    assert response.status_code == 200
    assert response.json() == [{
        "_id": "test",
        "title": "test",
        "author": "test",
        "synopsis": "test"
    }]


@pytest.mark.asyncio
async def test_get_mongo_one(client):
    response = await client.get("/mongo/test")
    assert response.status_code == 200
    assert response.json() == {
        "_id": "test",
        "title": "test",
        "author": "test",
        "synopsis": "test"
    }


@pytest.mark.asyncio
async def test_get_mongo_one_ID_NOT_FOUND(client):
    response = await client.get("/mongo/test1")
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_patch_mongo(client):
    response = await client.patch(
            "/mongo/test",
            json={
                "title": "test1",
                "author": "test1",
                "synopsis": "test1"
            },
        )
    assert response.status_code == 200
    assert response.json() == {
        "_id": "test",
        "title": "test1",
        "author": "test1",
        "synopsis": "test1"
    }


@pytest.mark.asyncio
async def test_patch_mongo_DATA_NOT_MODIFIED(client):
    response = await client.patch(
            "/mongo/test",
            json={
                "title": "test1",
                "author": "test1",
                "synopsis": "test1"
            },
        )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_patch_mongo_ID_NOT_FOUND(client):
    response = await client.patch(
            "/mongo/test1",
            json={
                "title": "test",
                "author": "test",
                "synopsis": "test"
            },
        )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_delete_mongo(client):
    response = await client.delete("/mongo/test")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_mongo_ID_NOT_FOUND(client):
    response = await client.delete("/mongo/test")
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login(client):
    response = await client.post(
            "/auth/token",
            data={
                "username": TEST_USER,
                "password": TEST_PASSWORD
            },
        )
    assert response.status_code == 200

    refresh_token = response.cookies
    access_token = response.json()["access_token"]

    assert access_token is not None
    return access_token, refresh_token


@pytest.mark.asyncio
async def test_get_postgres(client):
    access_token, refresh_token = await test_login(client)

    response = await client.get(
            "/postgres/",
            headers={
                "Authorization": f'Bearer {access_token}'
            },
            cookies=refresh_token
        )
    assert response.status_code == 200
    assert response.json() == []
