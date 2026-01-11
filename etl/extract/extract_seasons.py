import json
from etl.extract.api_client import fetch_json

def extract_seasons():
    data = fetch_json("/league/seasons.json")

    with open("data/raw/seasons.json", "w") as f:
        json.dump(data, f, indent=2)

    print("Seasons extracted successfully.")

if __name__ == "__main__":
    extract_seasons()
