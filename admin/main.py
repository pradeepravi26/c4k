import streamlit as st

st.set_page_config(
    page_title="Admin",
    page_icon=":guardsman:",
    layout="wide",
    initial_sidebar_state="expanded",
)

upload_users_page = st.Page(
    "user/upload_users.py",
    title="Upload Users",
    icon="📤",
)
manage_users_page = st.Page(
    "user/manage_users.py",
    title="Manage Users",
    icon="🔧",
)

pg = st.navigation(
    {
        "Home": [st.Page("home.py", title="Home", icon="🏠")],
        "Users": [upload_users_page, manage_users_page],
        "Member Visit": [
            st.Page(
                "member_visit/live_member_visits.py",
                title="Live Member Visits",
                icon="📊",
            ),
            st.Page(
                "member_visit/manage_member_visits.py",
                title="Manage Member Visits",
                icon="👥",
            ),
        ],
        "Forms": [
            st.Page(
                "forms/check_in.py",
                title="Check In",
                icon="📝",
            ),
            st.Page(
                "forms/check_out.py",
                title="Check Out",
                icon="📝",
            ),
        ],
    }
)

pg.run()
