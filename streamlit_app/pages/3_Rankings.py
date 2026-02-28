import streamlit as st
from db import run_query

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(page_title="Rankings", layout="wide")

st.title("🏆 Weekly AP Rankings")
st.caption("AP Top 25 rankings with filters, search, and team trends")


# --------------------------------------------------
# 1️⃣ Load Seasons
# --------------------------------------------------
season_query = """
SELECT DISTINCT season_year
FROM rankings
ORDER BY season_year DESC
"""

season_df = run_query(season_query)

if season_df.empty:
    st.warning("No rankings data available.")
    st.stop()

season = st.selectbox(
    "Season",
    season_df["season_year"]
)


# --------------------------------------------------
# 2️⃣ Load Weeks
# --------------------------------------------------
week_query = """
SELECT DISTINCT week
FROM rankings
WHERE season_year = %s
ORDER BY week
"""

week_df = run_query(week_query, params=(season,))

week = st.selectbox(
    "Week",
    week_df["week"]
)


# --------------------------------------------------
# 3️⃣ Rank Range
# --------------------------------------------------
rank_range = st.slider(
    "Rank Range",
    min_value=1,
    max_value=25,
    value=(1, 25)
)


# --------------------------------------------------
# 4️⃣ Search Team
# --------------------------------------------------
search = st.text_input(
    "🔍 Search team (name / market / alias)"
)


# --------------------------------------------------
# 5️⃣ Load ONLY Top 25 Rankings
# --------------------------------------------------
query = """
SELECT
    r.season_year,
    r.week,
    r.rank,
    r.points,
    r.fp_votes,
    r.wins,
    r.losses,
    t.team_id,
    t.name AS team_name,
    t.market AS team_market,
    t.alias AS team_alias
FROM rankings r
JOIN teams t
    ON r.team_id::uuid = t.team_id
WHERE r.season_year = %s
AND r.week = %s
AND r.rank BETWEEN %s AND %s
AND r.rank <= 25
"""

params = [
    season,
    week,
    rank_range[0],
    rank_range[1]
]


# Apply search filter safely
if search:
    query += """
    AND (
        t.name ILIKE %s
        OR t.market ILIKE %s
        OR t.alias ILIKE %s
    )
    """
    params.extend([
        f"%{search}%",
        f"%{search}%",
        f"%{search}%"
    ])


query += """
ORDER BY r.rank
LIMIT 25
"""


# FIX: convert list → tuple
df = run_query(query, params=tuple(params))


# --------------------------------------------------
# 6️⃣ Display Rankings Table
# --------------------------------------------------
st.subheader(f"📊 Rankings — Season {season}, Week {week}")

if df.empty:

    st.warning("No rankings found.")

else:

    st.dataframe(
        df[
            [
                "rank",
                "team_name",
                "team_market",
                "team_alias",
                "wins",
                "losses",
                "points",
                "fp_votes"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# 7️⃣ Summary Metrics
# --------------------------------------------------
if not df.empty:

    st.markdown("### 📌 Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Teams Ranked",
        df.shape[0]
    )

    col2.metric(
        "Avg Points",
        round(df["points"].mean(), 2)
    )

    col3.metric(
        "Total 1st Place Votes",
        int(df["fp_votes"].sum())
    )


# --------------------------------------------------
# 8️⃣ Team Ranking Trend (FIXED)
# --------------------------------------------------
st.markdown("### 📈 Team Ranking Trend")


# Load teams from rankings only (important fix)
team_query = """
SELECT DISTINCT t.team_id, t.name
FROM rankings r
JOIN teams t
    ON r.team_id::uuid = t.team_id
WHERE r.season_year = %s
ORDER BY t.name
"""

team_df = run_query(team_query, params=(season,))


team_selected = st.selectbox(
    "Select Team",
    team_df["name"]
)


# Get team_id safely
team_id = team_df.loc[
    team_df["name"] == team_selected,
    "team_id"
].values[0]


# Trend query FIXED using team_id instead of name
trend_query = """
SELECT
    r.week,
    r.rank
FROM rankings r
WHERE r.team_id::uuid = %s
AND r.season_year = %s
AND r.rank <= 25
ORDER BY r.week
"""

trend_df = run_query(
    trend_query,
    params=(team_id, season)
)


# Display chart
if not trend_df.empty:

    st.line_chart(
        trend_df.set_index("week")["rank"]
    )

else:

    st.info(
        "No ranking history available for this team."
    )