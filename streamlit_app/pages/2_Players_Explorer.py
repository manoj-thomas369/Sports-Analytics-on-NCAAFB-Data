import streamlit as st
from db import run_query

st.set_page_config(layout="wide")

st.title("👥 Players Explorer")
st.caption("Browse players, filter by position/status/eligibility, and search by name or team")

# --------------------------------------------------
# 📥 Load Players Data
# --------------------------------------------------
query = """
SELECT
  p.player_id,
  p.first_name,
  p.last_name,
  p.position,
  p.eligibility,
  p.height,
  p.weight,
  p.status,
  t.market || ' ' || t.name AS team
FROM players p
LEFT JOIN teams t ON p.team_id = t.team_id
ORDER BY p.last_name, p.first_name;
"""

df = run_query(query)

# --------------------------------------------------
# 🔍 Filters
# --------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    position_filter = st.selectbox(
        "Position",
        ["All"] + sorted(df["position"].dropna().unique().tolist())
    )

with col2:
    status_filter = st.selectbox(
        "Status",
        ["All"] + sorted(df["status"].dropna().unique().tolist())
    )

with col3:
    eligibility_filter = st.selectbox(
        "Eligibility",
        ["All"] + sorted(df["eligibility"].dropna().unique().tolist())
    )

search = st.text_input("🔎 Search player or team")

# --------------------------------------------------
# 🧠 Apply Filters
# --------------------------------------------------
filtered_df = df.copy()

if position_filter != "All":
    filtered_df = filtered_df[filtered_df["position"] == position_filter]

if status_filter != "All":
    filtered_df = filtered_df[filtered_df["status"] == status_filter]

if eligibility_filter != "All":
    filtered_df = filtered_df[filtered_df["eligibility"] == eligibility_filter]

if search:
    filtered_df = filtered_df[
        filtered_df["first_name"].str.contains(search, case=False, na=False)
        | filtered_df["last_name"].str.contains(search, case=False, na=False)
        | filtered_df["team"].str.contains(search, case=False, na=False)
    ]

# --------------------------------------------------
# 📊 Players Table
# --------------------------------------------------
st.subheader("🏈 Players")

st.dataframe(
    filtered_df[
        [
            "first_name",
            "last_name",
            "position",
            "eligibility",
            "height",
            "weight",
            "status",
            "team",
        ]
    ],
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# 📌 Summary
# --------------------------------------------------
st.caption(f"Showing {len(filtered_df)} players")
