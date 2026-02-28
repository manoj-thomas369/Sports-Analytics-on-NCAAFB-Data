import streamlit as st
from db import run_query

# --------------------------------------------------
# ⚙️ Page Config
# --------------------------------------------------
st.set_page_config(page_title="Venues", layout="wide")

st.title("🏟️ Venue Directory")
st.caption("Explore NCAA Football stadiums by location, capacity, and roof type")


# --------------------------------------------------
# 1️⃣ Load filter options (small queries)
# --------------------------------------------------
state_query = """
SELECT DISTINCT state
FROM venues
WHERE state IS NOT NULL
ORDER BY state
"""

roof_query = """
SELECT DISTINCT roof_type
FROM venues
WHERE roof_type IS NOT NULL
ORDER BY roof_type
"""

state_df = run_query(state_query)
roof_df = run_query(roof_query)


# --------------------------------------------------
# 2️⃣ Filters UI
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    state_filter = st.selectbox(
        "Filter by State",
        ["All"] + state_df["state"].tolist()
    )

with col2:
    roof_filter = st.selectbox(
        "Filter by Roof Type",
        ["All"] + roof_df["roof_type"].tolist()
    )


# --------------------------------------------------
# 3️⃣ Search input
# --------------------------------------------------
search = st.text_input("🔍 Search Venue or City")


# --------------------------------------------------
# 4️⃣ Load ONLY required venues from SQL
# --------------------------------------------------
query = """
SELECT
    venue_id,
    name,
    city,
    state,
    capacity,
    roof_type
FROM venues
WHERE 1=1
"""

params = []

if state_filter != "All":
    query += " AND state = %s"
    params.append(state_filter)

if roof_filter != "All":
    query += " AND roof_type = %s"
    params.append(roof_filter)

if search:
    query += """
    AND (
        name ILIKE %s
        OR city ILIKE %s
    )
    """
    params.append(f"%{search}%")
    params.append(f"%{search}%")

query += """
ORDER BY capacity DESC
LIMIT 500
"""


df = run_query(query, params=params)


# --------------------------------------------------
# 5️⃣ Display table
# --------------------------------------------------
st.subheader("📋 Stadium List")

if df.empty:
    st.warning("No venues found.")
else:
    st.dataframe(
        df[
            ["name", "city", "state", "capacity", "roof_type"]
        ],
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# 6️⃣ Summary metrics
# --------------------------------------------------
if not df.empty:

    st.markdown("### 📌 Summary")

    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric("Total Venues", df.shape[0])

    with m2:
        st.metric(
            "Avg Capacity",
            int(df["capacity"].mean())
        )

    with m3:
        st.metric(
            "Largest Stadium",
            int(df["capacity"].max())
        )