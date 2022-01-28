from peewee import *
from config.dbConfig import Base


class User(Base):
    id = AutoField()
    username = CharField()
    email = CharField()
    password = CharField()
    salt = CharField()
    token = CharField(null=True)
    token_expiry = IntegerField(null=True)
    acc_type = CharField()
    bio = CharField(default='')
    dob = CharField(default='')
    gender = CharField(default='')
    website = CharField(default='')
    location = CharField(default='')
    occupation = CharField(default='')
    followers = CharField(default='')
    following = CharField(default='')
    skills = CharField(default='')
    social_medias = CharField(default='')

    class Meta:
        database = Base._meta.db
        table_name = 'User'
