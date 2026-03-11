import pytest

@pytest.fixture
def sample_user():
    return {"name": "Ameen", "role": "developer", "active": True}


def test_user_greeting(sample_user):
    assert f"Hello, {sample_user['name']}" == f"Hello, {sample_user['name']}"

def test_user_is_active(sample_user):
    assert sample_user["active"] is True

def test_user_role(sample_user):
    assert sample_user["role"] == "developer"

def test_user_name_length(sample_user):
    assert len(sample_user["name"]) == 5