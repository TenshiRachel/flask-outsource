from peewee import *
from config.dbConfig import Base


class Job(Base):
    id = AutoField()
    sid = IntegerField()
    uid = IntegerField()
    uname = CharField()
    cid = IntegerField()
    cname = CharField()
    date = CharField()
    name = CharField()
    salary = DecimalField()
    remarks = CharField()
    status = CharField(default='unaccepted')

    class Meta:
        database = Base._meta.db
        table_name = 'Job'
