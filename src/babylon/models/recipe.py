from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from ..database import Base


class IngredientAssociation(Base):
    __tablename__ = "ingredient_association"
    recipe_id = Column(Integer, ForeignKey('recipe.id'), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredient.id'), primary_key=True)
    measured_in_id = Column(Integer, ForeignKey('measured_in.id'))
    amount = Column('amount', Integer)

    recipe = relationship("ModelRecipe", back_populates="ingredients")
    ingredient = relationship("ModelIngredient", back_populates="recipes")
    measured_in = relationship("ModelMeasuredIn", backref="measured_in")

tag_association_table = Table("tag_association", Base.metadata,
                          Column('recipe_id', Integer, ForeignKey('recipe.id')),
                          Column('tag_id', Integer, ForeignKey('tag.id')))


class ModelRecipe(Base):
    __tablename__ = "recipe"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, unique=True)
    ingredients = relationship("IngredientAssociation", back_populates="recipe")
    steps = Column('steps', String)
    description = Column('description', String)
    author = Column('author', String)
    tags = relationship("ModelTag",
                        secondary=tag_association_table,
                        backref="recipe")
    portions = Column('portions', Integer)

    def __init__(self, name, steps, description, author, portions):
        self.name = name
        self.steps = steps
        self.description = description
        self.author = author
        self.portions = portions