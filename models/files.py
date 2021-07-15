from peewee import *
from config.dbConfig import Base


class File(Base):
    id = AutoField()
    name = CharField()
    type = CharField()
    shareUid = CharField()
    uid = IntegerField()

    class Meta:
        database = Base._meta.db
        table_name = 'File'
