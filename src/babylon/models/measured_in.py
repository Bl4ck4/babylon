from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from ..database import Base
from .ingredient import ModelIngredient


class ModelMeasuredIn(Base):
    __tablename__ = "measured_in"

    id = Column('id', Integer, primary_key=True)
    measurement = Column('measurement', String, unique=True)

    # ingredientList = relationship(ModelIngredient, backref='measuredIn')

    def __init__(self, measurement):
        self.measurement = measurement
