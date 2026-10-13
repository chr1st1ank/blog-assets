from fastapi.testclient import TestClient

from hello_app.main import app


def test_hello() -> None:
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello, world!"}
