from peewee import *
from datetime import date
from config.dbConfig import Base
from models.user import User


class Portfolio(Base):
    id = AutoField()
    title = CharField()
    date = CharField(default=date.today().strftime('%d/%m/%Y'))
    content = CharField()
    category = CharField()
    views = IntegerField(default=0)
    likes = IntegerField(default=0)
    uid = ForeignKeyField(User)

    class Meta:
        database = Base._meta.db
        table_name = 'Portfolio'
