from etl.transform.transform_teams import transform_divisions_conferences_teams
from etl.load.db import engine
from etl.load.load_utils import load_dataframe

_, df_conferences, _ = transform_divisions_conferences_teams()
load_dataframe(df_conferences, "conferences", engine)
