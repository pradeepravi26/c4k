from typing import List
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
import pytz
from orm import User, MemberVisit
import uuid
from schema import UserOut
import datetime
from peewee import fn

local_tz = pytz.timezone("America/New_York")

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


# student check-in search page
@app.get("/users/check-in", response_model=List[UserOut])
def get_users_for_check_in(role: str):
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


# process check-in form submission
@app.post("/users/check-in/{user_id}")
def check_in_user(user_id: str, check_in_time: datetime.datetime):
    user = User.get_or_none(User.id == uuid.UUID(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    today = datetime.date.today()
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
        raise HTTPException(status_code=400, detail="User already checked in today")

    check_in_time = check_in_time.astimezone()

    in_time = datetime.datetime.combine(today, check_in_time.time())

    MemberVisit.create(
        user=user,
        in_time=in_time,
        out_time=None,
        calculated_duration="",
    )

    return {"success": True}


@app.get("/users/check-out", response_model=List[UserOut])
def get_users_for_check_out(role: str):
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

        if recent_visit:
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
            detail="No users available for check-out.",
        )

    return list(users.values())


@app.post("/users/check-out/{user_id}")
def check_out_user(user_id: str, check_out_time: datetime.datetime):
    user = User.get_or_none(User.id == uuid.UUID(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    today = datetime.date.today()
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
        raise HTTPException(status_code=400, detail="User not checked in today")

    check_out_time = check_out_time.astimezone()

    if check_out_time < local_tz.localize(recent_visit.in_time):
        raise HTTPException(
            status_code=400,
            detail="Check-out time cannot be earlier than check-in time",
        )

    now = datetime.datetime.now(local_tz)

    if check_out_time > now + datetime.timedelta(minutes=5):
        raise HTTPException(
            status_code=400,
            detail="Check-out time cannot be in the future",
        )

    out_time = datetime.datetime.combine(today, check_out_time.time())

    recent_visit.out_time = out_time
    recent_visit.save()

    return {"success": True}


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
