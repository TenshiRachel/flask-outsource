from config.dbConfig import Base
from models.user import User
from models.service import Service


def setupdb():
    Base._meta.db.connect()
    Base._meta.db.create_tables([User, Service])
    Base._meta.db.close()
