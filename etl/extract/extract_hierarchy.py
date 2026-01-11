import json
from etl.extract.api_client import fetch_json

def extract_hierarchy():
    data = fetch_json("/league/hierarchy.json")

    with open("data/raw/league_hierarchy.json", "w") as f:
        json.dump(data, f, indent=2)

    print("League hierarchy extracted successfully.")

if __name__ == "__main__":
    extract_hierarchy()
