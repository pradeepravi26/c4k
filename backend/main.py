from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from orm import User, MemberVisit
import uuid
from schema import UserOut
import datetime
from peewee import fn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/users/check-in", response_model=List[UserOut])
def get_users_by_role(role: str):
    if role not in ["student", "volunteer"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid role. Only 'student' or 'volunteer' roles are allowed.",
        )

    today = datetime.date.today()
    users = {}

    for user in User.select().where((User.role == role) & (User.is_active)):
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
            users[str(user.id.hex)] = {
                "id": str(user.id.hex),
                "full_name": user.full_name,
                "preferred_name": user.preferred_name,
                "c4k_id": user.c4k_id,
                "role": user.role,
                "is_active": user.is_active,
            }

    if not users:
        raise HTTPException(
            status_code=404,
            detail="No users available for check-in.",
        )

    return list(users.values())


@app.get("/users/{id}")
def get_user_by_id(id: str):
    user = User.get_or_none(User.id == uuid.UUID(id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": str(user.id.hex),
        "full_name": user.full_name,
        "preferred_name": user.preferred_name,
        "c4k_id": user.c4k_id,
        "role": user.role,
        "is_active": user.is_active,
    }
