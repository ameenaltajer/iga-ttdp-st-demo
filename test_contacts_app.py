import os
import tempfile
import pytest
 
import contacts_db
from contacts_app import app
from contacts_db import init_db
 
 
@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
 
    contacts_db.DB_NAME = db_path
    init_db()
 
    app.config["TESTING"] = True
 
    with app.test_client() as client:
        yield client
 
    os.close(db_fd)
    os.unlink(db_path)
 
 
def create_contact(client, name="Ameen", email="ameen@example.com", phone="12345678"):
    return client.post(
        "/contacts",
        json={"name": name, "email": email, "phone": phone}
    )
 
 
def test_get_contacts_empty_list(client):
    response = client.get("/contacts")
    assert response.status_code == 200
    assert response.get_json() == []
 
 
def test_create_valid_contact(client):
    response = create_contact(client)
    data = response.get_json()
 
    assert response.status_code == 201
    assert data["name"] == "Ameen"
    assert data["email"] == "ameen@example.com"
    assert data["phone"] == "12345678"
    assert "id" in data
 
 
def test_create_contact_missing_name(client):
    response = client.post(
        "/contacts",
        json={"email": "ameen@example.com", "phone": "12345678"}
    )
    assert response.status_code == 400
    assert "required" in response.get_json()["error"]
 
 
def test_create_contact_invalid_email(client):
    response = client.post(
        "/contacts",
        json={"name": "Ameen", "email": "bad-email", "phone": "12345678"}
    )
    assert response.status_code == 400
    assert response.get_json()["error"] == "invalid email"
 
 
 
def test_get_contacts_after_adding_three(client):
    create_contact(client, "A", "a@example.com", "111")
    create_contact(client, "B", "b@example.com", "222")
    create_contact(client, "C", "c@example.com", "333")
 
    response = client.get("/contacts")
    data = response.get_json()
 
    assert response.status_code == 200
    assert len(data) == 3
 
 
def test_get_contact_by_id(client):
    create_response = create_contact(client)
    contact_id = create_response.get_json()["id"]
 
    response = client.get(f"/contacts/{contact_id}")
    data = response.get_json()
 
    assert response.status_code == 200
    assert data["id"] == contact_id
    assert data["name"] == "Ameen"
 
 
def test_get_non_existing_contact(client):
    response = client.get("/contacts/999")
    assert response.status_code == 404
    assert response.get_json()["error"] == "contact not found"
 
 
def test_update_contact_name(client):
    create_response = create_contact(client)
    contact_id = create_response.get_json()["id"]
 
    response = client.put(f"/contacts/{contact_id}", json={"name": "Updated Ameen"})
    data = response.get_json()
 
    assert response.status_code == 200
    assert data["name"] == "Updated Ameen"
    assert data["email"] == "ameen@example.com"
    assert data["phone"] == "12345678"
 
 
def test_update_contact_phone(client):
    create_response = create_contact(client)
    contact_id = create_response.get_json()["id"]
 
    response = client.put(f"/contacts/{contact_id}", json={"phone": "99999999"})
    data = response.get_json()
 
    assert response.status_code == 200
    assert data["phone"] == "99999999"
 
 
def test_update_non_existing_contact(client):
    response = client.put("/contacts/999", json={"name": "Nobody"})
    assert response.status_code == 404
    assert response.get_json()["error"] == "contact not found"
 
 
def test_update_contact_invalid_email(client):
    create_response = create_contact(client)
    contact_id = create_response.get_json()["id"]
 
    response = client.put(f"/contacts/{contact_id}", json={"email": "not-an-email"})
    assert response.status_code == 400
    assert response.get_json()["error"] == "invalid email"
 
 
def test_delete_existing_contact(client):
    create_response = create_contact(client)
    contact_id = create_response.get_json()["id"]
 
    response = client.delete(f"/contacts/{contact_id}")
    assert response.status_code == 200
    assert response.get_json()["message"] == "contact deleted"
 
 
def test_deleted_contact_returns_404(client):
    create_response = create_contact(client)
    contact_id = create_response.get_json()["id"]
 
    client.delete(f"/contacts/{contact_id}")
    response = client.get(f"/contacts/{contact_id}")
 
    assert response.status_code == 404
    assert response.get_json()["error"] == "contact not found"
 
 
def test_delete_non_existing_contact(client):
    response = client.delete("/contacts/999")
    assert response.status_code == 404
    assert response.get_json()["error"] == "contact not found"
 
 
def test_search_by_name(client):
    create_contact(client, "Ameen Altajer", "ameen@example.com", "111")
    create_contact(client, "Sara Ahmed", "sara@example.com", "222")
 
    response = client.get("/contacts/search?q=Ameen")
    data = response.get_json()
 
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["name"] == "Ameen Altajer"
 
 
def test_search_by_email(client):
    create_contact(client, "Ameen", "ameen@example.com", "111")
    create_contact(client, "Sara", "sara@example.com", "222")
 
    response = client.get("/contacts/search?q=sara@")
    data = response.get_json()
 
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["email"] == "sara@example.com"
 
 
def test_search_no_results(client):
    create_contact(client, "Ameen", "ameen@example.com", "111")
 
    response = client.get("/contacts/search?q=notfound")
    data = response.get_json()
 
    assert response.status_code == 200
    assert data == []
 
 
def test_search_missing_query(client):
    response = client.get("/contacts/search")
    assert response.status_code == 400
    assert response.get_json()["error"] == "query parameter q is required"
 
 
def test_full_workflow(client):
    create_response = client.post(
        "/contacts",
        json={"name": "Initial", "email": "initial@example.com", "phone": "111"}
    )
    assert create_response.status_code == 201
    created = create_response.get_json()
    contact_id = created["id"]
 
    read_response = client.get(f"/contacts/{contact_id}")
    assert read_response.status_code == 200
    assert read_response.get_json()["name"] == "Initial"
 
    update_response = client.put(
        f"/contacts/{contact_id}",
        json={"name": "Updated", "phone": "999"}
    )
    assert update_response.status_code == 200
    assert update_response.get_json()["name"] == "Updated"
    assert update_response.get_json()["phone"] == "999"
 
    read_again = client.get(f"/contacts/{contact_id}")
    assert read_again.status_code == 200
    assert read_again.get_json()["name"] == "Updated"
 
    delete_response = client.delete(f"/contacts/{contact_id}")
    assert delete_response.status_code == 200
 
    confirm_gone = client.get(f"/contacts/{contact_id}")
    assert confirm_gone.status_code == 404
 