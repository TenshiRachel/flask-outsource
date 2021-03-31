from peewee import *
from config.dbConfig import Base


class User(Base):
    id = AutoField()
    username = CharField()
    email = CharField()
    password = CharField()
    acc_type = CharField()

    class Meta:
        database = Base._meta.db
        table_name = 'User'
