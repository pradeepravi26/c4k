import streamlit as st
from orm import MemberVisit, User
import datetime
from peewee import fn
import time

st.title("Live Member Visits")

today = datetime.date.today()

live_visits = (
    MemberVisit.select(MemberVisit, User)
    .join(User)
    .where(
        (fn.DATE(MemberVisit.in_time) == today) & (MemberVisit.out_time.is_null(True))
    )
    .order_by(MemberVisit.in_time.desc())
)

data = []

if live_visits.exists():
    data = [
        {
            "Full Name": visit.user.full_name,
            "Preferred Name": visit.user.preferred_name,
            "C4K ID": visit.user.c4k_id,
            "Role": visit.user.role,
            "Check-In Time": visit.in_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for visit in live_visits
    ]

if data:
    st.subheader("Members Currently Checked In")
    st.table(data)
else:
    st.info("No members are currently checked in.")

time.sleep(1)
st.rerun()
