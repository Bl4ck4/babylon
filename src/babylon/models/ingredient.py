from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class ModelIngredient(Base):
    __tablename__ = "ingredient"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, unique=True)
    recipes = relationship("IngredientAssociation", back_populates="ingredient")
    measured_in_id = Column(Integer, ForeignKey("measured_in.id"))
    measured_in = relationship("ModelMeasuredIn", back_populates="ingredients")

    def __init__(self, name, measured_in, *args, **kwargs):
        self.name = name
        self.measured_in = measured_in
