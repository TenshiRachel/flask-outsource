from peewee import *
from datetime import date
from config.dbConfig import Base


class Notification(Base):
    id = AutoField()
    uid = IntegerField()
    username = CharField()
    pid = IntegerField(default=None)
    title = CharField(default='')
    date = CharField(default=date.today().strftime('%d/%m/%Y'))
    category = CharField()
    user = IntegerField()

    class Meta:
        database = Base._meta.db
        table_name = 'Notification'
