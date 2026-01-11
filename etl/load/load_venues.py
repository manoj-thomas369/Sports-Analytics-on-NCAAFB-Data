import pandas as pd
from sqlalchemy import text
from etl.load.db import engine

FILE = "data/processed/venues.csv"

def load_venues():
    df = pd.read_csv(FILE)

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE venues CASCADE;"))

    df.to_sql(
        "venues",
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )

    print(f"✅ Loaded {len(df)} venues")

if __name__ == "__main__":
    load_venues()
