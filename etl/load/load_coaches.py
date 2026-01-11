from etl.transform.transform_coaches import transform_coaches
from etl.load.load_utils import load_dataframe
from etl.load.db import engine

def load_coaches():
    df = transform_coaches()
    load_dataframe(df, "coaches", engine)

if __name__ == "__main__":
    load_coaches()
