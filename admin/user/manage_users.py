import streamlit as st
from orm import User
import pandas as pd
import uuid

st.title("Manage Users")

users = list(User.select().where(User.role != "guest"))
user_data = [
    {
        "id": str(u.id.hex),
        "full_name": u.full_name,
        "preferred_name": u.preferred_name,
        "c4k_id": u.c4k_id,
        "role": u.role,
        "is_active": u.is_active,
    }
    for u in users
]

df = pd.DataFrame(user_data)

edited_df = st.data_editor(
    df,
    column_config={
        "id": st.column_config.Column(disabled=True),
        "role": st.column_config.SelectboxColumn(
            "Role",
            options=["student", "volunteer", "unassigned"],
            default="student",
            help="Select the role of the user",
            required=True,
        ),
    },
    use_container_width=True,
    num_rows="dynamic",
    height=1000,
)

changes = []

for index, row in edited_df.iterrows():
    # if row is added
    if index >= len(df) or pd.isna(row["id"]):
        user = User.create(
            full_name="unassigned",
            preferred_name="unassigned",
            c4k_id="unassigned",
            role="unassigned",
            is_active=True,
        )
        st.rerun()

    # if row is updated
    else:
        original_row = df.loc[index]
        diff = {
            col: {"old": original_row[col], "new": row[col]}
            for col in df.columns
            if original_row[col] != row[col]
        }

        if diff:
            user = User.get(User.id == row["id"])
            for field, change in diff.items():
                setattr(user, field, change["new"])
            user.save()
            st.rerun()

# if row is deleted
deleted_ids = set(df["id"]) - set(edited_df["id"].dropna())
for deleted_id in deleted_ids:
    try:
        user = User.get(User.id == deleted_id)
        user.delete_instance()
    except User.DoesNotExist:
        continue
