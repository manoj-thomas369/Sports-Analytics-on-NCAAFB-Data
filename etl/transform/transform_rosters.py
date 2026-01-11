import json
import pandas as pd
from pathlib import Path

RAW_ROSTERS_DIR = Path("data/raw/rosters")
OUTPUT_PATH = Path("data/processed/rosters.csv")


def transform_rosters():
    rows = []

    for file in RAW_ROSTERS_DIR.glob("*.json"):
        with open(file, "r") as f:
            data = json.load(f)

        team_id = data.get("id")

        for player in data.get("players", []):
            rows.append({
                "player_id": player.get("id"),
                "team_id": team_id
            })

    df = pd.DataFrame(rows).drop_duplicates()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    return df


if __name__ == "__main__":
    df = transform_rosters()
    print("Rosters:", df.shape)
    print(df.head())
