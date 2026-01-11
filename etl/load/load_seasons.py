import pandas as pd
from sqlalchemy import text
from etl.load.db import engine

FILE = "data/processed/seasons.csv"

def load_seasons():
    df = pd.read_csv(FILE)

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE seasons CASCADE;"))

    df.to_sql(
        "seasons",
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )

    print(f"✅ Loaded {len(df)} rows into seasons")


if __name__ == "__main__":
    load_seasons()
