import json
import os
import pandas as pd

RAW_ROSTERS_DIR = "data/raw/rosters"
OUT_FILE = "data/processed/coaches.csv"

def transform_coaches():
    rows = []

    for file in os.listdir(RAW_ROSTERS_DIR):
        path = os.path.join(RAW_ROSTERS_DIR, file)

        with open(path, "r") as f:
            data = json.load(f)

        team_id = data.get("id")  

        for coach in data.get("coaches", []):
            rows.append({
                "coach_id": coach.get("id"),
                "full_name": coach.get("full_name"),
                "position": coach.get("position"),
                "team_id": team_id
            })

    df = pd.DataFrame(rows).drop_duplicates(subset=["coach_id"])
    return df


if __name__ == "__main__":
    df = transform_coaches()
    df.to_csv(OUT_FILE, index=False)
    print(f"✅ Coaches processed: {df.shape}")
    print(df.head())
