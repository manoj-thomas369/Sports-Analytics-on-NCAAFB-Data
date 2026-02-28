import streamlit as st
from db import run_query

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="NCAA Football Data Explorer",
    layout="wide"
)

st.title("🏈 NCAA Football Data Explorer")
st.caption("Quick overview of teams, players, seasons, and venues")


# --------------------------------------------------
# TOP METRICS (FIXED)
# --------------------------------------------------
metrics_query = """
SELECT
    (SELECT COUNT(*) FROM teams) AS teams,

    (SELECT COUNT(*)
     FROM players
     WHERE status = 'ACT') AS active_players,

    (SELECT COUNT(*) FROM seasons) AS seasons,

    (SELECT COUNT(*) FROM venues) AS venues
"""

metrics_df = run_query(metrics_query)

if metrics_df.empty:
    st.error("Could not load metrics")
    st.stop()

metrics = metrics_df.iloc[0]


# Display metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("🏟️ Teams", metrics["teams"])

col2.metric("👥 Active Players", metrics["active_players"])

col3.metric("📅 Seasons", metrics["seasons"])

col4.metric("📍 Venues", metrics["venues"])


st.divider()


# --------------------------------------------------
# TEAMS SECTION
# --------------------------------------------------
st.subheader("🏫 Teams & Conferences")

search = st.text_input("🔍 Search by school or team")

teams_query = """
SELECT
    t.market AS school,
    t.name AS team,
    c.name AS conference,
    v.city,
    v.state
FROM teams t
LEFT JOIN conferences c
    ON t.conference_id::uuid = c.conference_id
LEFT JOIN venues v
    ON t.venue_id::uuid = v.venue_id
WHERE 1=1
"""

params = []

if search:

    teams_query += """
    AND (
        t.market ILIKE %s
        OR t.name ILIKE %s
    )
    """

    params.extend([
        f"%{search}%",
        f"%{search}%"
    ])

teams_query += """
ORDER BY t.market
LIMIT 200
"""

teams_df = run_query(
    teams_query,
    params=tuple(params)
)


if teams_df.empty:

    st.warning("No teams found")

else:

    st.dataframe(
        teams_df,
        use_container_width=True,
        hide_index=True
    )


st.divider()


# --------------------------------------------------
# SEASONS SECTION
# --------------------------------------------------
st.subheader("📅 Seasons Overview")

seasons_query = """
SELECT
    year,
    type_code AS season_type,
    status,
    start_date,
    end_date
FROM seasons
ORDER BY year DESC
LIMIT 50
"""

seasons_df = run_query(seasons_query)

if seasons_df.empty:

    st.warning("No seasons found")

else:

    st.dataframe(
        seasons_df,
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# Footer
# --------------------------------------------------
st.divider()

st.caption(
    "PostgreSQL backend • Streamlit frontend • Optimized queries"
)