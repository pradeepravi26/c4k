from peewee import *
import datetime


db = SqliteDatabase("c4k.db")


class BaseModel(Model):
    class Meta:
        database = db
