from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from ..database import Base


class ModelIngredient(Base):
    __tablename__ = "ingredient"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, unique=True)
    recipes = relationship("IngredientAssociation", back_populates="ingredient")

    def __init__(self, name):  # , amount):  # , measured_in_id):
        self.name = name
