import streamlit as st
from db import run_query

st.set_page_config(page_title="Coaches", layout="wide")

st.title("🧑‍🏫 Coaches Directory")
st.caption("Search and explore NCAA Football coaches and their teams")

# --------------------------------------------------
# 1️⃣ Load coaches data
# --------------------------------------------------
query = """
SELECT
    c.coach_id,
    c.full_name,
    c.position,
    t.name AS team_name,
    t.market AS team_market
FROM coaches c
LEFT JOIN teams t ON c.team_id = t.team_id
ORDER BY c.full_name;
"""

df = run_query(query)

if df.empty:
    st.warning("No coaches data available.")
    st.stop()

# --------------------------------------------------
# 2️⃣ Filters
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    position_filter = st.selectbox(
        "Filter by Position",
        ["All"] + sorted(df["position"].dropna().unique())
    )

with col2:
    team_filter = st.selectbox(
        "Filter by Team",
        ["All"] + sorted(df["team_name"].dropna().unique())
    )

if position_filter != "All":
    df = df[df["position"] == position_filter]

if team_filter != "All":
    df = df[df["team_name"] == team_filter]

# --------------------------------------------------
# 3️⃣ Search
# --------------------------------------------------
search = st.text_input("🔍 Search Coach or Team")

if search:
    df = df[
        df["full_name"].str.contains(search, case=False, na=False) |
        df["team_name"].str.contains(search, case=False, na=False) |
        df["team_market"].str.contains(search, case=False, na=False)
    ]

# --------------------------------------------------
# 4️⃣ Display table
# --------------------------------------------------
st.subheader("📋 Coaches List")

st.dataframe(
    df[
        ["full_name", "position", "team_market", "team_name"]
    ].rename(columns={
        "full_name": "Coach",
        "position": "Role",
        "team_market": "Team Market",
        "team_name": "Team Name"
    }).reset_index(drop=True),
    use_container_width=True
)

# --------------------------------------------------
# 5️⃣ Summary metrics
# --------------------------------------------------
st.markdown("### 📌 Summary")

m1, m2, m3 = st.columns(3)

with m1:
    st.metric("Total Coaches", df.shape[0])

with m2:
    st.metric("Unique Teams", df["team_name"].nunique())

with m3:
    st.metric("Coach Roles", df["position"].nunique())
