import json
import os
import pandas as pd

RAW_DIR = "data/raw/player_profiles"
OUT_PATH = "data/processed/player_statistics.csv"

def transform_player_statistics():
    rows = []

    for file in os.listdir(RAW_DIR):
        if not file.endswith(".json"):
            continue

        with open(os.path.join(RAW_DIR, file), "r") as f:
            data = json.load(f)

        player_id = data["id"]

        for season in data.get("seasons", []):
            season_id = season.get("id")

            for team in season.get("teams", []):
                team_id = team.get("id")
                stats = team.get("statistics", {})

                rows.append({
                    "player_id": player_id,
                    "team_id": team_id,
                    "season_id": season_id,

                    "games_played": stats.get("games_played"),
                    "games_started": stats.get("games_started"),

                    "rushing_yards": stats.get("rushing", {}).get("yards"),
                    "rushing_touchdowns": stats.get("rushing", {}).get("touchdowns"),

                    "receiving_yards": stats.get("receiving", {}).get("yards"),
                    "receiving_touchdowns": stats.get("receiving", {}).get("touchdowns"),

                    "kick_return_yards": stats.get("kick_returns", {}).get("yards"),
                    "fumbles": stats.get("fumbles", {}).get("fumbles"),
                })

    df = pd.DataFrame(rows)
    df.to_csv(OUT_PATH, index=False)

    print("✅ Player statistics transformed:", df.shape)
    return df

if __name__ == "__main__":
    transform_player_statistics()
