from unittest.mock import patch
from day2 import get_weather

@patch('day2.requests.get')
def test_get_weather(mock_get):
    # Mock response data
    mock_response = {
        "current": {
            "temperature_2m": 20,
            "wind_speed_10m": 5
        },
        "hourly": {
            "temperature_2m": [20, 21, 22],
            "relative_humidity_2m": [50, 55, 60],
            "wind_speed_10m": [5, 6, 7]
        }
    }
    
    # Configure the mock to return a response with the mocked data
    mock_get.return_value.json.return_value = mock_response
    
    # Call the function with test coordinates
    result = get_weather(40.7128, -74.0060)
    
    # Assert that the result matches the mocked response
    assert result == mock_response
    mock_get.assert_called_once()


