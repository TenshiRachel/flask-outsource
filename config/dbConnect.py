from config.dbConfig import Base
from models.user import User


def setupdb():
    Base._meta.db.connect()
    Base._meta.db.create_tables([User])
    Base._meta.db.close()
