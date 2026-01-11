import streamlit as st
from db import run_query

st.set_page_config(layout="wide")

st.title("🧩 Teams Explorer")
st.caption("Browse teams, filter by conference/division/state, and view rosters")

# --------------------------------------------------
# 📥 Load Teams Data
# --------------------------------------------------
query = """
SELECT
  t.team_id,
  t.market AS school,
  t.name AS team,
  t.alias,
  c.name AS conference,
  d.name AS division,
  v.name AS venue,
  v.city,
  v.state
FROM teams t
LEFT JOIN conferences c ON t.conference_id = c.conference_id
LEFT JOIN divisions d ON t.division_id = d.division_id
LEFT JOIN venues v ON t.venue_id = v.venue_id
ORDER BY school, team;
"""

df = run_query(query)

# --------------------------------------------------
# 🔍 Filters
# --------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    conference_filter = st.selectbox(
        "Conference",
        ["All"] + sorted(df["conference"].dropna().unique().tolist())
    )

with col2:
    division_filter = st.selectbox(
        "Division",
        ["All"] + sorted(df["division"].dropna().unique().tolist())
    )

with col3:
    state_filter = st.selectbox(
        "State",
        ["All"] + sorted(df["state"].dropna().unique().tolist())
    )

search = st.text_input("🔎 Search by team name or alias")

# --------------------------------------------------
# 🧠 Apply Filters
# --------------------------------------------------
filtered_df = df.copy()

if conference_filter != "All":
    filtered_df = filtered_df[filtered_df["conference"] == conference_filter]

if division_filter != "All":
    filtered_df = filtered_df[filtered_df["division"] == division_filter]

if state_filter != "All":
    filtered_df = filtered_df[filtered_df["state"] == state_filter]

if search:
    filtered_df = filtered_df[
        filtered_df["team"].str.contains(search, case=False, na=False)
        | filtered_df["alias"].str.contains(search, case=False, na=False)
    ]

# --------------------------------------------------
# 📊 Teams Table
# --------------------------------------------------
st.subheader("🏫 Teams")

st.dataframe(
    filtered_df[
        ["school", "team", "alias", "conference", "division", "venue", "state"]
    ],
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# 👥 Team Roster Viewer
# --------------------------------------------------
st.divider()
st.subheader("👥 View Team Roster")

team_options = filtered_df[["team_id", "school", "team"]].drop_duplicates()
team_options["label"] = team_options["school"] + " – " + team_options["team"]

selected_team = st.selectbox(
    "Select a team",
    options=team_options["label"]
)

if selected_team:
    team_id = team_options.loc[
        team_options["label"] == selected_team, "team_id"
    ].values[0]

    roster_query = """
    SELECT
      p.first_name,
      p.last_name,
      p.position,
      p.height,
      p.weight,
      p.status
    FROM rosters r
    JOIN players p ON r.player_id = p.player_id
    WHERE r.team_id = %s
    ORDER BY p.position, p.last_name;
    """

    roster_df = run_query(roster_query, params=(team_id,))

    st.dataframe(
        roster_df,
        use_container_width=True,
        hide_index=True
    )
