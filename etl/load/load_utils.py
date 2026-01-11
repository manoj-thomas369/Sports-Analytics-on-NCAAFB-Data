def load_dataframe(df, table_name, engine, if_exists="append"):
    """
    Generic utility to load a pandas DataFrame into PostgreSQL.

    Parameters:
    - df: pandas DataFrame
    - table_name: target table name in PostgreSQL
    - engine: SQLAlchemy engine
    - if_exists: 'append' | 'replace' | 'fail' (default: append)
    """
    df.to_sql(
        table_name,
        engine,
        if_exists=if_exists,
        index=False,
        method="multi"
    )

    print(f"Loaded {len(df)} rows into {table_name}")
