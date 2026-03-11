from unittest.mock import MagicMock, patch
from day2 import get_weather, get_multiple_cities
import requests


def test_error_handling():
    mock_response = MagicMock()
    mock_response.status_code = 503
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "503 Service Unavailable"
    )

    with patch("requests.get", return_value=mock_response):
        cities = [("New York", 40.71, -74.00)]
        results = get_multiple_cities(cities)

    assert results["New York"] is None
    print("✅ test_error_handling passed")