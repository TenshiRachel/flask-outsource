from peewee import *
from config.dbConfig import Base


class User(Base):
    id = IntegerField()
    username = CharField()
    password = CharField()

    class Meta:
        database = Base._meta.db
        table_name = 'User'
