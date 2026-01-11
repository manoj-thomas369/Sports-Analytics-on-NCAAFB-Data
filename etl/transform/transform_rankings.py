import json
import pandas as pd
import os

RAW_FILE = "data/raw/rankings_ap25_2025_week01.json"
OUT_FILE = "data/processed/rankings.csv"

def transform_rankings():
    with open(RAW_FILE, "r") as f:
        data = json.load(f)

    season_year = data["season"]
    week = data["week"]
    effective_time = data.get("effective_time")

    rows = []

    for entry in data.get("rankings", []):
        rows.append({
            "season_year": season_year,
            "week": week,
            "effective_time": effective_time,

            "team_id": entry.get("id"),

            "rank": entry.get("rank"),
            "prev_rank": entry.get("prev_rank"),

            "points": entry.get("points"),
            "fp_votes": entry.get("fp_votes"),

            "wins": entry.get("wins"),
            "losses": entry.get("losses"),
            "ties": entry.get("ties"),
        })

    df = pd.DataFrame(rows)
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(OUT_FILE, index=False)

    print(f"✅ Rankings transformed: {df.shape}")
    print(df.head())

    return df

if __name__ == "__main__":
    transform_rankings()
