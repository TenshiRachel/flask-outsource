from peewee import *
from config.dbConfig import Base
from models.user import User


class Follower(Base):
    follower_id = ForeignKeyField(User)
    following_id = ForeignKeyField(User)

    class Meta:
        database = Base._meta.db
        table_name = 'Follower'
        primary_key = CompositeKey('follower_id', 'following_id')
