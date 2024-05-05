from fastapi.testclient import TestClient

from main import app


def test_get_mongo():
    with TestClient(app) as client:
        response = client.get("/mongo/")
        assert response.status_code == 200

def test_get_mongo_1():
    with TestClient(app) as client:
        response = client.get("/mongo/0")
        assert response.status_code == 400
