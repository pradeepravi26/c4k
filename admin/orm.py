from peewee import (
    Model,
    SqliteDatabase,
    UUIDField,
    CharField,
    IntegerField,
    BooleanField,
    TextField,
    DateTimeField,
)
from playhouse.sqlite_ext import ForeignKeyField
import uuid


db = SqliteDatabase("../c4k.db")


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    full_name = CharField()
    preferred_name = CharField()
    c4k_id = CharField()
    role = CharField(choices=["student", "volunteer", "unassigned"])
    is_active = BooleanField(default=True)

    class Meta:
        table_name = "users"


class MemberVisit(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    user = ForeignKeyField(User, backref="visits", on_delete="CASCADE")
    in_time = DateTimeField()
    out_time = DateTimeField()
    calculated_duration = TextField()

    class Meta:
        table_name = "member_visits"
