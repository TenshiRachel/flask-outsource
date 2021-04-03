from peewee import *
from config.dbConfig import Base
from models.user import User


class Service(Base):
    id = AutoField()
    name = CharField()
    desc = CharField()
    price = DecimalField()
    categories = CharField()
    date_created = CharField()
    views = IntegerField()
    favs = IntegerField()
    uid = ForeignKeyField(User)

    class Meta:
        database = Base._meta.db
        table_name = 'Service'
