import requests, json
from datetime import datetime

VENMO_BASE = "https://api.venmo.com/v1"

class VenmoSession:
    def __init__(self, access_token):
        self.session = requests.Session()
        self.authenticated = True

        self.session.headers.update({
            "Authorization": f"Bearer {access_token}",
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        })

    def get_pending_requests(self):
        url = f"{VENMO_BASE}/payments"
        resp = self.session.get(url)

        if resp.status_code != 200:
            raise Exception(f"API error: {resp.status_code} {resp.text}")

        data = resp.json()
        r = []

        for d in data.get("data", []):
            if d["status"] == "pending" and d["action"] == "charge":

                r.append({
                    "id": d["id"],
                    "created": d["date_created"],
                    "username": d["target"]["user"]["username"],
                    "display_name": d["target"]["user"]["display_name"],
                    "amount": float(d["amount"]),
                    "note": d["note"]
                })

        return r