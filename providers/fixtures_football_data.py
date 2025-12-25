def get_scheduled_fixtures(token):
    url = f"{BASE_URL}/competitions/PL/matches"
    headers = {"X-Auth-Token": token}

    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()

    data = resp.json()

    # Filter scheduled fixtures locally (API does not support status filter)
    scheduled = [
        m for m in data.get("matches", [])
        if m.get("status") == "SCHEDULED"
    ]

    data["matches"] = scheduled
    return data
