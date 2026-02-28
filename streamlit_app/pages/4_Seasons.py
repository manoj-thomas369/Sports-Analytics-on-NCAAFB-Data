import streamlit as st
from db import run_query

# --------------------------------------------------
# ⚙️ Page Config
# --------------------------------------------------
st.set_page_config(layout="wide")

st.title("📅 Season & Schedule Viewer")
st.caption("Explore seasons, filter by year or status, and verify rankings availability")


# --------------------------------------------------
# 1️⃣ Load filter options first (small queries)
# --------------------------------------------------
year_query = """
SELECT DISTINCT year
FROM seasons
ORDER BY year DESC
"""

status_query = """
SELECT DISTINCT status
FROM seasons
ORDER BY status
"""

year_df = run_query(year_query)
status_df = run_query(status_query)


# --------------------------------------------------
# 2️⃣ Filters UI
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    year_filter = st.selectbox(
        "Season Year",
        ["All"] + year_df["year"].astype(str).tolist()
    )

with col2:
    status_filter = st.selectbox(
        "Season Status",
        ["All"] + status_df["status"].dropna().tolist()
    )


# --------------------------------------------------
# 3️⃣ Load ONLY required seasons from SQL
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
WHERE 1=1
"""

params = []

if year_filter != "All":
    query += " AND s.year = %s"
    params.append(int(year_filter))

if status_filter != "All":
    query += " AND s.status = %s"
    params.append(status_filter)

query += """
GROUP BY
    s.season_id,
    s.year,
    s.type_code,
    s.start_date,
    s.end_date,
    s.status
ORDER BY s.year DESC
LIMIT 200
"""


df = run_query(query, params=params)


# --------------------------------------------------
# 4️⃣ Display Seasons Table
# --------------------------------------------------
st.subheader("📆 Available Seasons")

if df.empty:
    st.warning("No seasons found.")
else:
    st.dataframe(
        df[
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
# 5️⃣ Summary metrics
# --------------------------------------------------
if not df.empty:

    st.markdown("### 📌 Summary")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Total Seasons", df.shape[0])

    with c2:
        st.metric(
            "Seasons with Rankings",
            df[df["rankings_count"] > 0].shape[0]
        )

    with c3:
        st.metric(
            "Latest Season",
            int(df["year"].max())
        )


# --------------------------------------------------
# 6️⃣ Notes
# --------------------------------------------------
st.caption(
    "• rankings_count > 0 means AP rankings exist\n"
    "• Seasons join Rankings via season_year\n"
    "• Filters are applied at database level for performance"
)