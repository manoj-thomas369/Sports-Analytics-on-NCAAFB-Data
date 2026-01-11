import streamlit as st
from db import run_query

st.set_page_config(page_title="Rankings", layout="wide")

st.title("🏆 Weekly AP Rankings")
st.caption("AP Top 25 rankings with filters, search, and team trends")

# --------------------------------------------------
# 1️⃣ Load rankings data
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
JOIN teams t ON r.team_id = t.team_id
ORDER BY r.season_year DESC, r.week, r.rank;
"""

df = run_query(query)

if df.empty:
    st.warning("No rankings data available.")
    st.stop()

# --------------------------------------------------
# 2️⃣ Filters (Season / Week / Rank range)
# --------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    season = st.selectbox(
        "Season",
        sorted(df["season_year"].unique(), reverse=True)
    )

with col2:
    week = st.selectbox(
        "Week",
        sorted(df[df["season_year"] == season]["week"].unique())
    )

with col3:
    rank_range = st.slider(
        "Rank Range",
        min_value=1,
        max_value=25,
        value=(1, 25)
    )

# --------------------------------------------------
# 3️⃣ Apply filters
# --------------------------------------------------
filtered_df = df[
    (df["season_year"] == season) &
    (df["week"] == week) &
    (df["rank"].between(rank_range[0], rank_range[1]))
].copy()

# --------------------------------------------------
# 4️⃣ Search by team
# --------------------------------------------------
search = st.text_input("🔍 Search team (name / market / alias)")

if search:
    filtered_df = filtered_df[
        filtered_df["team_name"].str.contains(search, case=False, na=False) |
        filtered_df["team_market"].str.contains(search, case=False, na=False) |
        filtered_df["team_alias"].str.contains(search, case=False, na=False)
    ]

# --------------------------------------------------
# 5️⃣ Rankings table
# --------------------------------------------------
st.subheader(f"📊 Rankings — Season {season}, Week {week}")

st.dataframe(
    filtered_df[
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
    ].reset_index(drop=True),
    use_container_width=True
)

# --------------------------------------------------
# 6️⃣ Summary metrics
# --------------------------------------------------
st.markdown("### 📌 Summary")

m1, m2, m3 = st.columns(3)

with m1:
    st.metric("Teams Ranked", filtered_df.shape[0])

with m2:
    st.metric("Avg Points", round(filtered_df["points"].mean(), 2))

with m3:
    st.metric("Total 1st Place Votes", int(filtered_df["fp_votes"].sum()))

# --------------------------------------------------
# 7️⃣ Team ranking trend (by week)
# --------------------------------------------------
st.markdown("### 📈 Team Ranking Trend")

team_selected = st.selectbox(
    "Select a Team",
    sorted(df["team_name"].unique())
)

trend_df = df[
    (df["team_name"] == team_selected) &
    (df["season_year"] == season)
].sort_values("week")

if not trend_df.empty:
    st.line_chart(
        trend_df.set_index("week")["rank"]
    )
else:
    st.info("No ranking history available for this team in this season.")
