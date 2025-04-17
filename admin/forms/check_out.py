import streamlit as st
from orm import MemberVisit, User
import datetime
from peewee import fn


if "check_in_time" not in st.session_state:
    st.session_state["check_in_time"] = datetime.datetime.now().time()

st.title("Check Out")

user_role = st.selectbox(
    "Select User Type",
    options=["student", "volunteer", "guest"],
    label_visibility="collapsed",
)

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

    if recent_visit:
        if user_role == "guest":
            users[str(user.id.hex)] = f"{user.full_name}"
        else:
            users[str(user.id.hex)] = f"{user.full_name} ({user.c4k_id})"

if not users:
    st.warning("No users available for check-out.")
    st.stop()

user = st.selectbox(
    "Select User",
    options=users.values(),
    label_visibility="collapsed",
)

user_id = [k for k, v in users.items() if v == user][0]
selected_user = User.get(User.id == user_id)

recent_visit = (
    MemberVisit.select()
    .where(
        (MemberVisit.user == selected_user)
        & (fn.DATE(MemberVisit.in_time) == today)
        & (MemberVisit.out_time.is_null(True))
    )
    .order_by(MemberVisit.in_time.desc())
    .first()
)

if recent_visit:
    st.info(f"Check-In Time: {recent_visit.in_time.strftime('%Y-%m-%d %H:%M:%S')}")

    check_out_time = st.time_input(
        "Select Check-Out Time",
        value=st.session_state["check_in_time"],
        step=datetime.timedelta(minutes=1),
    )

    if check_out_time:
        check_out_datetime = datetime.datetime.combine(today, check_out_time)
        if check_out_datetime < recent_visit.in_time:
            st.error("Check-out time cannot be earlier than the check-in time.")
        else:
            if st.button("Check Out", use_container_width=True):
                recent_visit.out_time = check_out_datetime
                recent_visit.calculated_duration = str(
                    check_out_datetime - recent_visit.in_time
                )
                recent_visit.save()
                st.success("Check-Out Successful")
                st.balloons()
