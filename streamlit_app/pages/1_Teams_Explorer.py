import streamlit as st
from db import run_query

# --------------------------------------------------
# ⚙️ Page Config
# --------------------------------------------------
st.set_page_config(layout="wide")

st.title("🧩 Teams Explorer")
st.caption("Browse teams, filter by conference/division/state, and view rosters")


# --------------------------------------------------
# 🔍 Filters UI
# --------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    conference_filter = st.text_input("Conference")

with col2:
    division_filter = st.text_input("Division")

with col3:
    state_filter = st.text_input("State")

search = st.text_input("🔎 Search by team name or alias")


# --------------------------------------------------
# 📥 Load ONLY REQUIRED Teams from SQL
# --------------------------------------------------
teams_query = """
SELECT
    t.team_id,
    t.market AS school,
    t.name AS team,
    t.alias,
    c.name AS conference,
    d.name AS division,
    v.name AS venue,
    v.state
FROM teams t
LEFT JOIN conferences c
    ON t.conference_id::uuid = c.conference_id
LEFT JOIN divisions d
    ON t.division_id::uuid = d.division_id
LEFT JOIN venues v
    ON t.venue_id::uuid = v.venue_id
WHERE 1=1
"""

params = []

# Apply filters dynamically
if conference_filter:
    teams_query += " AND c.name ILIKE %s"
    params.append(f"%{conference_filter}%")

if division_filter:
    teams_query += " AND d.name ILIKE %s"
    params.append(f"%{division_filter}%")

if state_filter:
    teams_query += " AND v.state ILIKE %s"
    params.append(f"%{state_filter}%")

if search:
    teams_query += " AND (t.name ILIKE %s OR t.alias ILIKE %s)"
    params.append(f"%{search}%")
    params.append(f"%{search}%")

teams_query += " ORDER BY school, team LIMIT 500"


# Execute query
df = run_query(teams_query, params=params)


# --------------------------------------------------
# 📊 Display Teams Table
# --------------------------------------------------
st.subheader("🏫 Teams")

if df.empty:
    st.warning("No teams found.")
else:
    st.dataframe(
        df[[
            "school",
            "team",
            "alias",
            "conference",
            "division",
            "venue",
            "state"
        ]],
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# 👥 Team Roster Viewer
# --------------------------------------------------
st.divider()
st.subheader("👥 View Team Roster")

if not df.empty:

    # Create dropdown labels
    df["label"] = df["school"] + " – " + df["team"]

    selected_team = st.selectbox(
        "Select a team",
        options=df["label"]
    )

    if selected_team:

        team_id = df.loc[
            df["label"] == selected_team,
            "team_id"
        ].values[0]

        # --------------------------------------------------
        # Load roster ONLY for selected team
        # --------------------------------------------------
        roster_query = """
        SELECT
            p.first_name,
            p.last_name,
            p.position,
            p.height,
            p.weight,
            p.status
        FROM rosters r
        JOIN players p
            ON r.player_id::uuid = p.player_id
        WHERE r.team_id::uuid = %s
        ORDER BY p.position, p.last_name
        """

        roster_df = run_query(
            roster_query,
            params=(team_id,)
        )

        if roster_df.empty:
            st.warning("No roster found for this team.")
        else:
            st.dataframe(
                roster_df,
                use_container_width=True,
                hide_index=True
            )