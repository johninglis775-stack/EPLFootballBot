import requests

BASE_URL = "https://api.football-data.org/v4"

def get_scheduled_fixtures(token):
    url = f"{BASE_URL}/competitions/PL/matches"
    headers = {"X-Auth-Token": token}
    params = {"status": "SCHEDULED"}

    resp = requests.get(url, headers=headers, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()
