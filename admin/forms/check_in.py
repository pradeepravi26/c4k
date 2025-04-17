import streamlit as st
from orm import MemberVisit, User
import datetime
from peewee import fn

if "check_in_time" not in st.session_state:
    st.session_state["check_in_time"] = datetime.datetime.now().time()

st.title("Check In")

user_role = st.selectbox(
    "Select User Type",
    options=["student", "volunteer", "guest"],
    label_visibility="collapsed",
)

if user_role == "student" or user_role == "volunteer":
    users = {}
    today = datetime.date.today()

    for user in User.select().where((User.role == user_role) & (User.is_active)):
        recent_visit = (
            MemberVisit.select()
            .where(
                (MemberVisit.user == user)
                & (fn.DATE(MemberVisit.in_time) == today)
                & (MemberVisit.out_time.is_null(True))
            )
            .order_by(MemberVisit.in_time.desc())
            .first()
        )

        if not recent_visit:
            users[str(user.id.hex)] = f"{user.full_name} ({user.c4k_id})"

    if not users:
        st.warning("No users available for check-in.")
        st.stop()

    user = st.selectbox(
        "Select User",
        options=users.values(),
        label_visibility="collapsed",
    )


if user_role == "guest":
    guest = st.text_input(
        "Enter Guest Name",
        placeholder="Enter Guest Name",
        label_visibility="collapsed",
    )
    check_in_date = st.date_input("Check In Date", datetime.date.today())
    check_in_time = st.time_input(
        "Check In Time",
        value=st.session_state["check_in_time"],
        step=datetime.timedelta(minutes=1),
    )
    st.session_state["check_in_time"] = check_in_time

    if guest and check_in_date and check_in_time:
        button = st.button(
            "Check In",
            use_container_width=True,
        )
        if button:
            guest_user = User.create(
                full_name=guest,
                role="guest",
            )
            MemberVisit.create(
                user=guest_user,
                in_time=datetime.datetime.combine(check_in_date, check_in_time),
                out_time=None,
                calculated_duration="",
            )
            st.success("Check In Successful")
            st.balloons()
            del st.session_state["check_in_time"]

if user_role == "student" or user_role == "volunteer":
    user_id = [k for k, v in users.items() if v == user][0]
    check_in_date = st.date_input("Check In Date", datetime.date.today())
    check_in_time = st.time_input(
        "Check In Time",
        st.session_state["check_in_time"],
        step=datetime.timedelta(minutes=1),
    )
    st.session_state["check_in_time"] = check_in_time

    if check_in_date and check_in_time:
        button = st.button(
            "Check In",
            use_container_width=True,
        )
        if button:
            user = User.get(User.id == user_id)
            MemberVisit.create(
                user=user,
                in_time=datetime.datetime.combine(check_in_date, check_in_time),
                out_time=None,
                calculated_duration="",
            )
            st.success("Check In Successful")
            st.balloons()
            del st.session_state["check_in_time"]
