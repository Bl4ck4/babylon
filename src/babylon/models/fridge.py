from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship
from ..database import Base


fridge_ingredient_association_table = Table("fridge_ingredient_association", Base.metadata,
                                            Column("fridge_id", Integer, ForeignKey("fridge.id")),
                                            Column("ingredient_id", Integer, ForeignKey("ingredient.id")))

class ModelFridge(Base):

    __tablename__ = "fridge"
    id = Column('id', Integer, primary_key=True)
    ingredients = relationship("ModelIngredient",
                               secondary=fridge_ingredient_association_table,
                               backref="fridge")