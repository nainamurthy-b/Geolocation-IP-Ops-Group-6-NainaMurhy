import requests
from epita_naina_murthy.config import config


def fetch_live_data() -> dict:
    config.validate()

    url = "https://ipinfo.io/json"

    headers = {
        "Authorization": f"Bearer {config.api_key}"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    return {
        "status": "LIVE_SUCCESS",
        "ip": data.get("ip", "Unknown"),
        "city": data.get("city", "Unknown"),
        "region": data.get("region", "Unknown"),
        "country": data.get("country", "Unknown"),
        "organization": data.get("org", "Unknown"),
        "postal": data.get("postal", "Unknown"),
        "timezone": data.get("timezone", "Unknown")
    }