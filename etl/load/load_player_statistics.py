import pandas as pd
from sqlalchemy import text
from etl.load.db import engine

FILE = "data/processed/player_statistics.csv"

def load_player_statistics():
    df = pd.read_csv(FILE)

    with engine.begin() as conn:
        conn.execute(text("SET session_replication_role = 'replica';"))
        conn.execute(text("TRUNCATE TABLE player_statistics;"))

    df.to_sql(
        "player_statistics",
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )

    with engine.begin() as conn:
        conn.execute(text("SET session_replication_role = 'origin';"))

    print(f"✅ Loaded {len(df)} rows into player_statistics")

if __name__ == "__main__":
    load_player_statistics()
