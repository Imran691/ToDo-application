from fastapi.testclient import TestClient
from app.main import app


def test_root_path():
    client = TestClient(app = app)
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_root_path_1():
    client = TestClient(app = app)
    response = client.get("/")
    assert response.status_code == 200  
    assert response.json() == {"message": "Hello"}