import streamlit as st
from orm import MemberVisit, User
import datetime
from peewee import fn
import time

if "start_date" not in st.session_state:
    st.session_state["start_date"] = datetime.datetime.now().date()

if "end_date" not in st.session_state:
    st.session_state["end_date"] = datetime.datetime.now().date()

st.title("Manage Member Visits")

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

if len(date_range) == 2:
    st.session_state["start_date"] = date_range[0]
    st.session_state["end_date"] = date_range[1]

if len(date_range) == 1:
    st.info("If you want to select a single date, please select the same date twice.")

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

        # Display the data in a table
        st.subheader("Member Visits")
        st.dataframe(visits_data)
    else:
        st.info("No member visits found for the selected filters.")
else:
    st.warning("Please select a valid date range and user roles.")
