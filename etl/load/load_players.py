import pandas as pd
from etl.load.db import engine

def load_players():
    df = pd.read_csv("data/processed/players.csv")

    df.to_sql(
        "players",
        engine,
        if_exists="append",   #NEVER replace parent tables
        index=False,
        method="multi"
    )

    print(f"✅ Loaded {len(df)} players")

if __name__ == "__main__":
    load_players()
