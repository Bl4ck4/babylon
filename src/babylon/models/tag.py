from sqlalchemy import Column, Integer, String
from ..database import Base


class ModelTag(Base):
    __tablename__ = "tag"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, unique=True)

    def __init__(self, name):
        self.name = name