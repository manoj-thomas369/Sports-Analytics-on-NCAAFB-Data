import json
import os
from etl.extract.api_client import fetch_json

YEARS = [2021, 2022, 2023]
SEASON_TYPE = "REG"   

OUTPUT_DIR = "data/raw/schedules"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_schedules():
    for year in YEARS:
        print(f"Fetching {SEASON_TYPE} schedule for {year}...")
        endpoint = f"/games/{year}/{SEASON_TYPE}/schedule.json"
        data = fetch_json(endpoint)

        output_path = os.path.join(OUTPUT_DIR, f"schedule_{year}_{SEASON_TYPE}.json")
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)

        print(f"Saved {output_path}")

if __name__ == "__main__":
    extract_schedules()
