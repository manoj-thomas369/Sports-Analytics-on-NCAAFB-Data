import json
import pandas as pd

INPUT_FILE = "data/raw/league_hierarchy.json"
OUTPUT_FILE = "data/processed/venues.csv"

def transform_venues():
    with open(INPUT_FILE, "r") as f:
        data = json.load(f)

    rows = []

    for division in data.get("divisions", []):
        for conference in division.get("conferences", []):
            for team in conference.get("teams", []):
                venue = team.get("venue")
                if not venue:
                    continue

                rows.append({
                    "venue_id": venue.get("id"),
                    "name": venue.get("name"),
                    "city": venue.get("city"),
                    "state": venue.get("state"),
                    "country": venue.get("country"),
                    "zip": venue.get("zip"),
                    "address": venue.get("address"),
                    "capacity": venue.get("capacity"),
                    "surface": venue.get("surface"),
                    "roof_type": venue.get("roof_type"),
                    "lat": venue.get("location", {}).get("lat"),
                    "lng": venue.get("location", {}).get("lng"),
                })

    df = pd.DataFrame(rows).drop_duplicates(subset=["venue_id"])
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Venues processed: {df.shape}")

if __name__ == "__main__":
    transform_venues()
