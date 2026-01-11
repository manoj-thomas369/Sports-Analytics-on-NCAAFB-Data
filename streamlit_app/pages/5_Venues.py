import streamlit as st
from db import run_query

st.set_page_config(page_title="Venues", layout="wide")

st.title("🏟️ Venue Directory")
st.caption("Explore NCAA Football stadiums by location, capacity, and roof type")

# --------------------------------------------------
# 1️⃣ Load venues data
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
ORDER BY capacity DESC;
"""

df = run_query(query)

if df.empty:
    st.warning("No venue data available.")
    st.stop()

# --------------------------------------------------
# 2️⃣ Filters
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    state_filter = st.selectbox(
        "Filter by State",
        ["All"] + sorted(df["state"].dropna().unique())
    )

with col2:
    roof_filter = st.selectbox(
        "Filter by Roof Type",
        ["All"] + sorted(df["roof_type"].dropna().unique())
    )

# Apply filters
if state_filter != "All":
    df = df[df["state"] == state_filter]

if roof_filter != "All":
    df = df[df["roof_type"] == roof_filter]

# --------------------------------------------------
# 3️⃣ Search venue
# --------------------------------------------------
search = st.text_input("🔍 Search Venue or City")

if search:
    df = df[
        df["name"].str.contains(search, case=False, na=False) |
        df["city"].str.contains(search, case=False, na=False)
    ]

# --------------------------------------------------
# 4️⃣ Display table
# --------------------------------------------------
st.subheader("📋 Stadium List")

st.dataframe(
    df[
        ["name", "city", "state", "capacity", "roof_type"]
    ].reset_index(drop=True),
    use_container_width=True
)

# --------------------------------------------------
# 5️⃣ Summary metrics
# --------------------------------------------------
st.markdown("### 📌 Summary")

m1, m2, m3 = st.columns(3)

with m1:
    st.metric("Total Venues", df.shape[0])

with m2:
    st.metric("Avg Capacity", int(df["capacity"].mean()))

with m3:
    st.metric("Largest Stadium", int(df["capacity"].max()))
