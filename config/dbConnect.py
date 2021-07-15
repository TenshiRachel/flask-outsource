from config.dbConfig import Base
from models.user import User
from models.service import Service
from models.job import Job
from models.files import File


def setupdb():
    Base._meta.db.connect()
    Base._meta.db.create_tables([User, Service, Job, File])
    Base._meta.db.close()
