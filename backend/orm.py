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
    full_name = CharField(null=True)
    preferred_name = CharField(null=True)
    c4k_id = CharField(null=True)
    role = CharField(choices=["student", "volunteer", "unassigned", "guest"], null=True)
    is_active = BooleanField(default=True)

    class Meta:
        table_name = "users"


class MemberVisit(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    user = ForeignKeyField(User, backref="visits", on_delete="CASCADE")
    in_time = DateTimeField(null=True)
    out_time = DateTimeField(null=True)
    calculated_duration = TextField(null=True)

    class Meta:
        table_name = "member_visits"


if __name__ == "__main__":
    db.connect()
    db.drop_tables([User, MemberVisit], safe=True)
    db.create_tables([User, MemberVisit], safe=True)
    db.close()
