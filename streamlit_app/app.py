import streamlit as st
from db import run_query

st.set_page_config(
    page_title="NCAA Football Data Explorer",
    layout="wide"
)

st.title("🏈 NCAA Football Data Explorer")
st.caption("Quick overview of teams, players, and seasons")

# -----------------------------
# 📊 TOP METRICS
# -----------------------------
metrics_query = """
SELECT
  (SELECT COUNT(*) FROM teams) AS teams,
  (SELECT COUNT(*) FROM players WHERE status = 'ACT') AS active_players,
  (SELECT COUNT(*) FROM seasons) AS seasons,
  (SELECT COUNT(*) FROM venues) AS venues;
"""

metrics = run_query(metrics_query).iloc[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric("🏟️ Teams", metrics["teams"])
col2.metric("👥 Active Players", metrics["active_players"])
col3.metric("📅 Seasons", metrics["seasons"])
col4.metric("📍 Venues", metrics["venues"])

st.divider()

# -----------------------------
# 🏫 TEAMS & CONFERENCES
# -----------------------------
st.subheader("🏫 Teams & Conferences")

teams_query = """
SELECT
  t.market AS school,
  t.name AS team,
  c.name AS conference,
  v.city,
  v.state
FROM teams t
LEFT JOIN conferences c ON t.conference_id = c.conference_id
LEFT JOIN venues v ON t.venue_id = v.venue_id
ORDER BY school;
"""

teams_df = run_query(teams_query)

search = st.text_input("🔍 Search by school or team name")
if search:
    teams_df = teams_df[
        teams_df["school"].str.contains(search, case=False, na=False) |
        teams_df["team"].str.contains(search, case=False, na=False)
    ]

st.dataframe(
    teams_df,
    use_container_width=True,
    hide_index=True
)

st.divider()

# -----------------------------
# 📅 SEASONS OVERVIEW
# -----------------------------
st.subheader("📅 Seasons Overview")

seasons_query = """
SELECT
  year,
  type_code AS season_type,
  status,
  start_date,
  end_date
FROM seasons
ORDER BY year DESC;
"""

seasons_df = run_query(seasons_query)

st.dataframe(
    seasons_df,
    use_container_width=True,
    hide_index=True
)
