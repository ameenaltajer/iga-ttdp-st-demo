from unittest.mock import patch
from day2 import send_email
import day2


@pytest.fixture(autouse=True)
def clean_db(tmp_path, monkeypatch):
    """Redirect the database to a temp file for every test."""
    db_file = str(tmp_path / "db.json")
    monkeypatch.setattr("user_service.DATABASE_FILE", db_file)
    yield



@patch("day2.send_email")
def test_send_email(mock_send_email):
    # The real function (NotImplementedError) is replaced
    # mock_send_email does nothing — no crash
    day2.send_email("ameen.altajer@hotmail.com", "Welcome!", "Thank you for signing up!")

    mock_send_email.assert_called_once_with(
        "ameen.altajer@hotmail.com",
        "Welcome!",
        "Thank you for signing up!"
    )