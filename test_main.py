from fastapi. testclient import TestClient
from main import app

client = TestClient(app)   

def test_read_main():
     response = client.get("/items/")
     assert response. status_code == 200
     assert response.json() == response.json()
    