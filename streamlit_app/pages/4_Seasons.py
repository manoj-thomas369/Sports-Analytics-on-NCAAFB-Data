import streamlit as st
from db import run_query

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(layout="wide")

st.title("📅 Season & Schedule Viewer")
st.caption("Explore seasons and verify rankings availability")


# --------------------------------------------------
# Load seasons with correct rankings count
# --------------------------------------------------
query = """
SELECT
    s.season_id,
    s.year,
    s.type_code,
    s.start_date,
    s.end_date,
    s.status,

    COUNT(DISTINCT r.week) AS rankings_count

FROM seasons s

LEFT JOIN rankings r
    ON s.year = r.season_year

GROUP BY
    s.season_id,
    s.year,
    s.type_code,
    s.start_date,
    s.end_date,
    s.status

ORDER BY s.year DESC
"""

df = run_query(query)


# --------------------------------------------------
# Filters
# --------------------------------------------------
col1, col2 = st.columns(2)

year_filter = col1.selectbox(
    "Season Year",
    ["All"] + df["year"].astype(str).tolist()
)

status_filter = col2.selectbox(
    "Season Status",
    ["All"] + df["status"].dropna().tolist()
)


# Apply filters
filtered_df = df.copy()

if year_filter != "All":
    filtered_df = filtered_df[
        filtered_df["year"] == int(year_filter)
    ]

if status_filter != "All":
    filtered_df = filtered_df[
        filtered_df["status"] == status_filter
    ]


# --------------------------------------------------
# Display table
# --------------------------------------------------
st.subheader("📆 Available Seasons")

st.dataframe(
    filtered_df[
        [
            "year",
            "type_code",
            "status",
            "start_date",
            "end_date",
            "rankings_count"
        ]
    ],
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# Summary (FIXED)
# --------------------------------------------------
st.markdown("### 📌 Summary")

total_seasons = filtered_df.shape[0]

# Correct logic: count seasons with rankings_count > 0
seasons_with_rankings = filtered_df[
    filtered_df["rankings_count"] > 0
].shape[0]

latest_season = filtered_df["year"].max()

c1, c2, c3 = st.columns(3)

c1.metric("Total Seasons", total_seasons)

c2.metric("Seasons with Rankings", seasons_with_rankings)

c3.metric("Latest Season", latest_season)


# --------------------------------------------------
# Notes
# --------------------------------------------------
st.caption(
    "• rankings_count shows number of ranked weeks\n"
    "• > 0 means rankings exist for that season\n"
    "• Data fetched directly from PostgreSQL"
)