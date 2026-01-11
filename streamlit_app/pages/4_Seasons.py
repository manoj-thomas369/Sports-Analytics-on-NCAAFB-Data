import streamlit as st
from db import run_query

st.set_page_config(layout="wide")

st.title("📅 Season & Schedule Viewer")
st.caption("Explore seasons, filter by year or status, and verify rankings availability")

# --------------------------------------------------
# 📥 Load Seasons (with ranking availability)
# --------------------------------------------------
query = """
SELECT
    s.season_id,
    s.year,
    s.type_code,
    s.start_date,
    s.end_date,
    s.status,
    COUNT(r.rank) AS rankings_count
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
ORDER BY s.year DESC;
"""

df = run_query(query)

# --------------------------------------------------
# 🎛 Filters
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    year_filter = st.selectbox(
        "Season Year",
        ["All"] + sorted(df["year"].unique().tolist(), reverse=True)
    )

with col2:
    status_filter = st.selectbox(
        "Season Status",
        ["All"] + sorted(df["status"].dropna().unique().tolist())
    )

# --------------------------------------------------
# 🧠 Apply Filters
# --------------------------------------------------
filtered_df = df.copy()

if year_filter != "All":
    filtered_df = filtered_df[filtered_df["year"] == year_filter]

if status_filter != "All":
    filtered_df = filtered_df[filtered_df["status"] == status_filter]

# --------------------------------------------------
# 📊 Seasons Table
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
# 📌 Notes
# --------------------------------------------------
st.caption(
    "• `rankings_count` > 0 means AP rankings exist for that season\n"
    "• Seasons are joinable with Rankings via `season_year`"
)
