from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from orm import User, MemberVisit
import uuid
from schema import UserOut

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


@app.get("/users", response_model=List[UserOut])
def get_users_by_role(role: str):
    users = list(User.select().where((User.role == role) & (User.is_active)))
    if not users:
        raise HTTPException(
            status_code=404,
            detail="No users found with the specified role and active status",
        )
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
    return user_data


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
