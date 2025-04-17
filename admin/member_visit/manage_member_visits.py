import streamlit as st
from orm import MemberVisit, User
import datetime
from peewee import fn
import time
import pandas as pd

if "start_date" not in st.session_state:
    st.session_state["start_date"] = datetime.datetime.now().date()

if "end_date" not in st.session_state:
    st.session_state["end_date"] = datetime.datetime.now().date()

if "visits_data" not in st.session_state:
    st.session_state["visits_data"] = "No data available"

col1, col2 = st.columns([5, 1], vertical_alignment="bottom")
with col1:
    st.title("Manage Member Visits")
with col2:
    st.download_button(
        label="Download CSV",
        data=st.session_state["visits_data"],
        file_name="data.csv",
        mime="text/csv",
        icon=":material/download:",
        use_container_width=True,
    )

user_roles = st.multiselect(
    "Select User Type",
    options=["student", "volunteer", "guest"],
    default=["student", "volunteer", "guest"],
    label_visibility="collapsed",
)

date_range = st.date_input(
    "Select Date Range",
    value=(st.session_state["start_date"], st.session_state["end_date"]),
    label_visibility="collapsed",
)

if st.session_state["start_date"] and st.session_state["end_date"] and user_roles:
    visits_query = (
        MemberVisit.select(MemberVisit, User)
        .join(User)
        .where(
            (fn.DATE(MemberVisit.in_time) >= st.session_state["start_date"])
            & (fn.DATE(MemberVisit.in_time) <= st.session_state["end_date"])
            & (User.role.in_(user_roles))
        )
        .order_by(MemberVisit.in_time.desc())
    )

    # Prepare data for display
    if visits_query.exists():
        visits_data = [
            {
                "Full Name": visit.user.full_name,
                "Preferred Name": visit.user.preferred_name,
                "C4K ID": visit.user.c4k_id,
                "Role": visit.user.role,
                "Check-In Time": visit.in_time.strftime("%Y-%m-%d %H:%M:%S"),
                "Check-Out Time": visit.out_time.strftime("%Y-%m-%d %H:%M:%S")
                if visit.out_time
                else "N/A",
                "Duration": visit.calculated_duration or "N/A",
            }
            for visit in visits_query
        ]

        st.session_state["visits_data"] = pd.DataFrame(visits_data).to_csv(index=False)

        st.subheader("Member Visits")
        st.dataframe(visits_data)

    else:
        st.info("No member visits found for the selected filters.")
else:
    st.warning("Please select a valid date range and user roles.")
