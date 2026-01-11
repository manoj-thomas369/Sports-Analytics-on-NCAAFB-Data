import json
import os
import pandas as pd

ROSTERS_DIR = "data/raw/rosters"
OUT_FILE = "data/processed/players.csv"

def transform_players():
    rows = []

    for file in os.listdir(ROSTERS_DIR):
        path = os.path.join(ROSTERS_DIR, file)

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        team_id = data.get("id")  
        players = data.get("players", [])

        if not team_id or not players:
            continue

        for p in players:
            rows.append({
                "player_id": p.get("id"),
                "first_name": p.get("first_name"),
                "last_name": p.get("last_name"),
                "abbr_name": p.get("abbr_name"),
                "birth_place": p.get("birth_place"),
                "position": p.get("position"),
                "height": p.get("height"),
                "weight": p.get("weight"),
                "status": p.get("status"),
                "eligibility": p.get("eligibility"),
                "team_id": team_id
            })

    df = pd.DataFrame(rows).drop_duplicates(subset=["player_id"])
    df.to_csv(OUT_FILE, index=False)

    print("✅ Players transformed:", df.shape)
    print(df[["player_id", "team_id"]].head())

    return df

if __name__ == "__main__":
    transform_players()
