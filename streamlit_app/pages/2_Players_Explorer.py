import streamlit as st
from db import run_query

# --------------------------------------------------
# ⚙️ Page Config
# --------------------------------------------------
st.set_page_config(layout="wide")

st.title("👥 Players Explorer")
st.caption("Browse players, filter by position/status/eligibility, and search by name or team")


# --------------------------------------------------
# 🔍 Filters UI
# --------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    position_filter = st.text_input("Position")

with col2:
    status_filter = st.text_input("Status")

with col3:
    eligibility_filter = st.text_input("Eligibility")

search = st.text_input("🔎 Search player or team")


# --------------------------------------------------
# 📥 Load ONLY REQUIRED Players from SQL
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
LEFT JOIN teams t
  ON p.team_id::uuid = t.team_id
WHERE 1=1
"""

params = []

# Apply filters in SQL
if position_filter:
    query += " AND p.position ILIKE %s"
    params.append(f"%{position_filter}%")

if status_filter:
    query += " AND p.status ILIKE %s"
    params.append(f"%{status_filter}%")

if eligibility_filter:
    query += " AND p.eligibility ILIKE %s"
    params.append(f"%{eligibility_filter}%")

if search:
    query += """
    AND (
        p.first_name ILIKE %s
        OR p.last_name ILIKE %s
        OR (t.market || ' ' || t.name) ILIKE %s
    )
    """
    params.append(f"%{search}%")
    params.append(f"%{search}%")
    params.append(f"%{search}%")

query += " ORDER BY p.last_name, p.first_name LIMIT 1000"


# Execute query
df = run_query(query, params=params)


# --------------------------------------------------
# 📊 Display Players Table
# --------------------------------------------------
st.subheader("🏈 Players")

if df.empty:
    st.warning("No players found.")
else:
    st.dataframe(
        df[
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
st.caption(f"Showing {len(df)} players")