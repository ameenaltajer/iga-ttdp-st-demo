import pytest
import requests
from api_service import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_api_response(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json() == {"message": "Hi!"}