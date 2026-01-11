import pandas as pd
import os
from sqlalchemy import create_engine

# Streamlit Cloud → secrets.toml
# Local → fallback URL

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:holyroot@localhost:5432/ncaafb_db"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

def run_query(query, params=None):
    with engine.connect() as conn:
        return pd.read_sql(query, conn, params=params)
