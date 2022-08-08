import os
from config.dbConfig import Base
from models.user import User
from models.portfolio import Portfolio
from models.comment import Comment
from models.service import Service
from models.job import Job
from models.filesFolders import File
from models.notifications import Notification


def setupdb():
    if not os.path.exists('./data'):
        os.makedirs('./data', exist_ok=True)
    Base._meta.db.connect()
    Base._meta.db.create_tables([User, Portfolio, Comment, Service, Job, File, Notification])
    print('Tables created')
    Base._meta.db.close()
