from database import *
import pytest
import os
from api_service import app



@pytest.fixture
def client():
    with app.test_client() as client:
        yield client





def test_check_db_health(client):
    response = client.get("/db_health")
    assert response.status_code == 200
    assert response.get_json() == {"message": "Hi, Ameen!"}
    


def test_get_all_users(client):
    response = client.get("/get_users")
    assert response.status_code == 200
    assert "users" in response.get_json()
    

def test_all_users_not_empty(client):
    response = client.get("/get_users")
    assert response.status_code == 200
    users = response.get_json().get("users", [])
    assert len(users) > 0