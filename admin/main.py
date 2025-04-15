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
    "user/manage_users_page.py",
    title="Manage Users",
    icon="🔧",
)

pg = st.navigation(
    {
        "Home": [st.Page("home.py", title="Home", icon="🏠")],
        "Users": [upload_users_page, manage_users_page],
    }
)

pg.run()
