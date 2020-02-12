import datetime
import bcrypt
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from ..database import Base


class User(Base):
    __tablename__ = "user"

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    username = Column('username', String(255), unique=True, nullable=False)
    email = Column('email', String(255), unique=True, nullable=False)
    password = Column('password', String(255), nullable=False)
    registered_on = Column('registered_on', DateTime(), nullable=False)
    admin = Column('admin', Boolean(), nullable=False, default=False)

    def __init__(self, username, email, password, admin=False):
        self.username = username
        self.email = email
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(password.encode("UTF-8"), salt)
        self.registered_on = datetime.datetime.now()
        self.admin = admin
