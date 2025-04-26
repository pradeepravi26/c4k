import streamlit as st

st.title("Welcome to the Admin Dashboard")
st.markdown("""
### Overview
This dashboard allows administrators to manage users, track member visits, and handle check-in/check-out processes efficiently.

Use the navigation menu on the left to access different sections of the dashboard.
""")

st.divider()
st.subheader("User Management")
st.markdown("""
- Upload student and volunteer data
- View, edit, or download user data
""")

st.subheader("Member Visits")
st.markdown("""
- View live member visits
- Manage and download visit data
""")

st.subheader("Forms")
st.markdown("""
- Check-in members
- Check-out members
""")

st.divider()

st.info("Use the navigation menu to explore the dashboard.")
