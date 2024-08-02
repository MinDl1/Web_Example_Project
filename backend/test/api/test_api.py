from fastapi.testclient import TestClient

from test_config import TEST_USER, TEST_PASSWD
from main import app


access_token, refresh_token = None, None


def test_get_mongo():
    with TestClient(app) as client:
        response = client.get("/mongo/")
        assert response.status_code == 200


def test_get_mongo_1():
    with TestClient(app) as client:
        response = client.get("/mongo/0")
        assert response.status_code == 400


def test_login():
    global access_token, refresh_token

    with TestClient(app) as client:
        response = client.post(
            "/auth/token",
            data={
                "username": TEST_USER,
                "password": TEST_PASSWD
            },
        )
        assert response.status_code == 200

        refresh_token = response.cookies
        access_token = response.json()["access_token"]

        assert access_token is not None
        return access_token, refresh_token


def test_get_postgres():
    global access_token, refresh_token

    with TestClient(app) as client:
        response = client.get(
            "/postgres/",
            headers={
                "Authorization": f'Bearer {access_token}'
            },
            cookies=refresh_token
        )
        assert response.status_code == 200
        assert response.json() == []
