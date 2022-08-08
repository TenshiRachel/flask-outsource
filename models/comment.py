from peewee import *
from datetime import date
from config.dbConfig import Base


class Comment(Base):
    id = AutoField()
    uid = IntegerField()
    username = CharField()
    content = CharField()
    pid = IntegerField()
    date = CharField(default=date.today().strftime('%d/%m/%Y'))

    class Meta:
        database = Base._meta.db
        table_name = 'Comment'
