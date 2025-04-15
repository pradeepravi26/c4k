import streamlit as st
import pandas as pd
from orm import User

st.title("Upload Users")

if "csv_file" not in st.session_state:
    st.session_state.csv_file = None

user_type = st.selectbox(
    "Select User Type",
    options=["student", "volunteer"],
    label_visibility="collapsed",
)

csv_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"],
    label_visibility="collapsed",
)

if csv_file != st.session_state.csv_file:
    st.session_state.csv_file = csv_file
    st.session_state.validated = False

if csv_file is not None:
    df = pd.read_csv(csv_file, header=None)
    df.columns = ["full_name", "preferred_name", "c4k_id"]
    st.dataframe(df)

    if st.button("Validate", use_container_width=True):
        csv_users = df.to_dict(orient="records")
        for user in csv_users:
            user["role"] = user_type
            user["is_active"] = True

        # user_data_json = pd.Series(user_data).to_json(orient="records")
        # st.json(user_data_json)

        user_c4k_ids_db = []
        for user in User.select():
            user_c4k_ids_db.append(user.c4k_id)

        # user_c4k_ids_csv = {}
        # for user in csv_users:
        #     user_c4k_ids_csv.append(user["c4k_id"])

        user_c4k_ids_csv = {}
        for user in csv_users:
            if user["c4k_id"] in user_c4k_ids_csv:
                user_c4k_ids_csv[user["c4k_id"]] += 1
            else:
                user_c4k_ids_csv[user["c4k_id"]] = 1

        user_in_db_count = 0
        new_user_count = 0
        is_valid = True
        duplicates = set()
        for user in csv_users:
            if user["c4k_id"] in user_c4k_ids_db:
                # st.error(f"c4k_id already exists in database: {user['c4k_id']}")
                user_in_db_count += 1
            elif (
                user["c4k_id"] in user_c4k_ids_csv
                and user_c4k_ids_csv[user["c4k_id"]] > 1
            ):
                # st.error(f"c4k_id already exists in CSV: {user['c4k_id']}")
                duplicates.add(user["c4k_id"])
                is_valid = False

        for duplicate in duplicates:
            st.error(
                f"Duplicate c4k_id found in CSV: {duplicate} ({user_c4k_ids_csv[duplicate]} times)"
            )

        if is_valid:
            st.session_state.validated = True
            st.session_state.csv_users = csv_users
            st.session_state.user_in_db_count = user_in_db_count
            st.session_state.upload_success = False
            # st.success("CSV is valid")
            # st.info(
            #     f"{len(csv_users) - user_in_db_count} users to be added, {user_in_db_count} already in database"
            # )
        else:
            st.session_state.validated = False

if st.session_state.get("validated", False):
    st.success("CSV is valid")
    st.info(
        f"{len(st.session_state.csv_users) - st.session_state.user_in_db_count} users to be added, {st.session_state.user_in_db_count} already in database"
    )
    if st.button("Upload", use_container_width=True):
        # csv_users = st.session_state.csv_users
        user_c4k_ids_db = [user.c4k_id for user in User.select()]

        for user in st.session_state.csv_users:
            if user["c4k_id"] not in user_c4k_ids_db:
                User.create(
                    full_name=user["full_name"],
                    preferred_name=user["preferred_name"],
                    c4k_id=user["c4k_id"],
                    role=user_type,
                    is_active=True,
                )

        st.session_state.validated = False
        st.session_state.csv_users = None
        st.session_state.user_in_db_count = 0
        st.session_state.upload_success = True
        st.rerun()

if st.session_state.get("upload_success", False):
    st.success("Users uploaded successfully")
