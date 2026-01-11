import json
import pandas as pd

INPUT_FILE = "data/raw/league_hierarchy.json"
OUTPUT_FILE = "data/processed/teams.csv"

def transform_teams():
    with open(INPUT_FILE, "r") as f:
        data = json.load(f)

    rows = []

    for division in data.get("divisions", []):
        division_id = division.get("id")

        for conference in division.get("conferences", []):
            conference_id = conference.get("id")

            for team in conference.get("teams", []):
                venue = team.get("venue")

                rows.append({
                    "team_id": team.get("id"),
                    "market": team.get("market"),
                    "name": team.get("name"),
                    "alias": team.get("alias"),
                    "founded": team.get("founded"),
                    "mascot": team.get("mascot"),
                    "fight_song": team.get("fight_song"),
                    "championships_won": team.get("championships_won"),
                    "conference_id": conference_id,
                    "division_id": division_id,
                    "venue_id": venue.get("id") if venue else None,
                })

    df = pd.DataFrame(rows).drop_duplicates(subset=["team_id"])
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Teams processed: {df.shape}")

if __name__ == "__main__":
    transform_teams()
