import pandas as pd
from sqlalchemy import text
from etl.load.db import engine

FILE = "data/processed/rankings.csv"

def load_rankings():
    df = pd.read_csv(FILE)

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE rankings;"))

    df.to_sql(
        "rankings",
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )

    print(f"✅ Loaded {len(df)} rows into rankings")

if __name__ == "__main__":
    load_rankings()
