from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from ..database import Base


class ModelMeasuredIn(Base):
    __tablename__ = "measured_in"

    id = Column('id', Integer, primary_key=True)
    measurement = Column('measurement', String, unique=True)
    ingredients = relationship("ModelIngredient", back_populates="measured_in")

    def __init__(self, measurement):
        self.measurement = measurement
