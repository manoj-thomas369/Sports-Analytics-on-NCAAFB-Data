import json
import os
import time
from etl.extract.api_client import fetch_json

HIERARCHY_FILE = "data/raw/league_hierarchy.json"
OUTPUT_DIR = "data/raw/rosters"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_team_ids():
    with open(HIERARCHY_FILE, "r") as f:
        data = json.load(f)

    team_ids = []
    for division in data.get("divisions", []):
        for conference in division.get("conferences", []):
            for team in conference.get("teams", []):
                team_ids.append(team["id"])

    return team_ids


def extract_rosters():
    team_ids = get_team_ids()
    print(f"Found {len(team_ids)} teams")

    for team_id in team_ids:
        output_path = os.path.join(OUTPUT_DIR, f"{team_id}.json")

        #Skip already downloaded teams
        if os.path.exists(output_path):
            continue

        print(f"Fetching full roster for team {team_id}")
        data = fetch_json(f"/teams/{team_id}/full_roster.json")

        if data is None:
            continue

        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)

        print(f"Saved roster for {team_id}")
        time.sleep(0.5)  # be polite to the API


if __name__ == "__main__":
    extract_rosters()
