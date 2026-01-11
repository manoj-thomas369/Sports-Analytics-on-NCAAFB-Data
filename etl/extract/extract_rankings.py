import json
from etl.extract.api_client import fetch_json

OUTPUT_FILE = "data/raw/rankings_ap25_2025_week01.json"

def extract_rankings():
    print("Fetching AP25 rankings for 2025 Week 01...")

    data = fetch_json("/polls/AP25/2025/01/rankings.json")

    if data is None:
        print("Rankings unavailable.")
        return

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print("Rankings extracted successfully.")

if __name__ == "__main__":
    extract_rankings()
