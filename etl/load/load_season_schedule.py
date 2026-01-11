from etl.transform.transform_schedule import transform_schedule
from etl.load.load_utils import load_dataframe
from etl.load.db import engine

def load_season_schedule():
    df_schedule = transform_schedule()

    load_dataframe(
        df_schedule,
        "season_schedule",
        engine
    )

if __name__ == "__main__":
    load_season_schedule()
