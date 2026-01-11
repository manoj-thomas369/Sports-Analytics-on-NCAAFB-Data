import json
import os
import time
from etl.extract.api_client import fetch_json

#configurable parameters
ROSTERS_DIR = "data/raw/rosters"
OUTPUT_DIR = "data/raw/player_profiles"
MAX_PLAYERS = 50          # max profiles to fetch in one run
SLEEP_TIME = 0.7          # polite delay for trial API
# ------------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)


def get_player_ids():
    """
    Extract unique player IDs from all roster JSON files.
    Handles multiple Sportradar roster structures safely.
    """
    player_ids = set()

    for file in os.listdir(ROSTERS_DIR):
        path = os.path.join(ROSTERS_DIR, file)

        if not file.endswith(".json"):
            continue

        with open(path, "r") as f:
            data = json.load(f)

        # Case 1: players at top level
        if "players" in data:
            players = data.get("players", [])

        # Case 2: players nested under roster
        elif "roster" in data and "players" in data["roster"]:
            players = data["roster"]["players"]

        else:
            players = []

        for player in players:
            if isinstance(player, dict) and "id" in player:
                player_ids.add(player["id"])

    return list(player_ids)


def extract_player_profiles():
    player_ids = get_player_ids()
    print(f"Found {len(player_ids)} unique players in rosters")

    fetched = 0

    for player_id in player_ids:
        if fetched >= MAX_PLAYERS:
            print("Reached MAX_PLAYERS limit. Stopping.")
            break

        output_path = os.path.join(OUTPUT_DIR, f"{player_id}.json")

        # Skip already fetched profiles
        if os.path.exists(output_path):
            continue

        print(f"Fetching profile for player {player_id}")
        data = fetch_json(f"/players/{player_id}/profile.json")

        # Skip if API failed / rate-limited / unavailable
        if data is None:
            continue

        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)

        print(f"Saved profile for {player_id}")
        fetched += 1
        time.sleep(SLEEP_TIME)

    print(f"Finished. Total profiles saved: {fetched}")


if __name__ == "__main__":
    extract_player_profiles()
