import json
import pandas as pd

RAW_FILE = "data/raw/seasons.json"
OUT_FILE = "data/processed/seasons.csv"

def transform_seasons():
    with open(RAW_FILE, "r") as f:
        data = json.load(f)

    rows = []

    for season in data.get("seasons", []):
        rows.append({
            "season_id": season.get("id"),
            "year": season.get("year"),
            "start_date": season.get("start_date"),
            "end_date": season.get("end_date"),
            "status": season.get("status"),
            "type_code": season.get("type", {}).get("code")
        })

    df = pd.DataFrame(rows)
    return df


if __name__ == "__main__":
    df = transform_seasons()
    df.to_csv(OUT_FILE, index=False)
    print(f"✅ Seasons processed: {df.shape}")
    print(df.head())
