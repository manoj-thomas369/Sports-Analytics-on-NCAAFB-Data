import json
import os
import pandas as pd

SCHEDULES_DIR = "data/raw/schedules"

def transform_schedule():
    rows = []

    for file in os.listdir(SCHEDULES_DIR):
        path = os.path.join(SCHEDULES_DIR, file)

        with open(path, "r") as f:
            data = json.load(f)

        season_year = data.get("year")

        for week in data.get("weeks", []):
            for game in week.get("games", []):
                rows.append({
                    "game_id": game.get("id"),
                    "season_year": season_year,
                    "scheduled": game.get("scheduled"),
                    "status": game.get("status"),
                    "home_team_id": game.get("home", {}).get("id"),
                    "away_team_id": game.get("away", {}).get("id"),
                    "venue_id": game.get("venue", {}).get("id")
                })

    df_schedule = pd.DataFrame(rows).drop_duplicates(subset=["game_id"])
    return df_schedule


if __name__ == "__main__":
    df = transform_schedule()
    print("Schedule:", df.shape)
    print(df.head())
