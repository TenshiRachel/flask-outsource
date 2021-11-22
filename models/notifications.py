from peewee import *
from config.dbConfig import Base


class Notification(Base):
    id = AutoField()
    uid = IntegerField()
    username = CharField()
    pid = IntegerField()
    title = CharField()
    date = CharField()
    category = CharField()

    class Meta:
        database = Base._meta.db
        table_name = 'Notification'
