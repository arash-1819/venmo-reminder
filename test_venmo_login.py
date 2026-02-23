from venmo_api import VenmoSession
import os
from dotenv import load_dotenv

load_dotenv()

VENMO_ACCESS_TOKEN = os.getenv("VENMO_ACCESS_TOKEN")

def main():
    vs = VenmoSession(VENMO_ACCESS_TOKEN)

    print("Fetching pending requests...")
    pending = vs.get_pending_requests()
    print(f"Found {len(pending)} pending requests.")

if __name__ == "__main__":
    main()