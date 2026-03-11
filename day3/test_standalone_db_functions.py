from database import *
import pytest
import os


@pytest.fixture
def setup_db():
    if os.path.exists("example.db"):
        os.remove("example.db")
    init_db()
    yield
    if os.path.exists("example.db"):
        os.remove("example.db")


def test_init_db_creates_table(setup_db):
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    table = cursor.fetchone()
    conn.close()

    assert table is not None


def test_add_user(setup_db):
    add_user("Ameen")

    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users WHERE name=?", ("Ameen",))
    user = cursor.fetchone()
    conn.close()

    assert user[0] == "Ameen"


def test_delete_user(setup_db):
    add_user("Ameen")
    delete_user(1)

    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=1")
    user = cursor.fetchone()
    conn.close()

    assert user is None


def test_get_all_users(setup_db):
    add_user("Ameen")
    add_user("Sara")

    users = get_all_users()

    assert len(users) == 2
    assert users[0][1] == "Ameen"
    assert users[1][1] == "Sara"
