import pandas as pd
from sqlalchemy import text
from etl.load.db import engine

FILE = "data/processed/teams.csv"

def load_teams():
    df = pd.read_csv(FILE)

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE teams CASCADE;"))

    df.to_sql(
        "teams",
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )

    print(f"✅ Loaded {len(df)} teams")

if __name__ == "__main__":
    load_teams()
