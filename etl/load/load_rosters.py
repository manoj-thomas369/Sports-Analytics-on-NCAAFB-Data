import pandas as pd
from etl.load.db import engine
from etl.load.load_utils import load_dataframe


def load_rosters():
    df = pd.read_csv("data/processed/rosters.csv")
    load_dataframe(df, "rosters", engine)


if __name__ == "__main__":
    load_rosters()
