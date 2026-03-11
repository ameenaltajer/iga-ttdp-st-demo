import requests

def get_weather(latitude, longitude):
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        f"&current_weather=true"
    )
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data["current_weather"]


def get_multiple_cities(cities):
    results = {}
    for name, lat, lon in cities:
        try:
            results[name] = get_weather(lat, lon)
        except requests.exceptions.HTTPError:
            results[name] = None
    return results