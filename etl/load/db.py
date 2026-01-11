from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:holyroot@localhost:5432/ncaafb_db"

engine = create_engine(DATABASE_URL)
