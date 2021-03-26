from peewee import *
from config import db


class Base(Model):
    class Meta:
        db = SqliteDatabase(db.params['name'])
