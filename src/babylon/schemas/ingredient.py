from graphene_sqlalchemy import SQLAlchemyObjectType
import graphene
from ..database import db_session
from ..models import ModelIngredient, IngredientAssociation
from ..lib.utils import input_to_dictionary
from importlib import import_module
from flask_jwt_extended import jwt_required


class IngredientAttributes:
    name = graphene.String(description="Name of Ingredient")
    amount = graphene.Float(description="Amount of this ingredient")
    measured_in = graphene.String(description="What is this ingredient measured in")


class Ingredient(SQLAlchemyObjectType, IngredientAttributes):

    recipes = graphene.List(lambda: import_module('.recipe', "babylon.schemas").Recipe)
    fridges = graphene.List(lambda: import_module('.fridge', "babylon.schemas").Fridge)

    @graphene.resolve_only_args
    def resolve_recipes(self):
        return [recipe.recipe for recipe in self.recipes]

    @graphene.resolve_only_args
    def resolve_fridges(self):
        return [fridge for fridge in self.fridge]

    @graphene.resolve_only_args
    def resolve_amount(self):
        return db_session.query(IngredientAssociation) \
            .filter(IngredientAssociation.ingredient_id==self.id) \
            .first() \
            .amount

    @graphene.resolve_only_args
    def resolve_measured_in(self):
        return db_session.query(IngredientAssociation) \
            .filter(IngredientAssociation.ingredient_id==self.id) \
            .first() \
            .ingredient.measured_in.measurement

    class Meta:
        model = ModelIngredient
        interfaces = (graphene.relay.Node,)


class CreateIngredientInput(graphene.InputObjectType, IngredientAttributes):
    pass


class CreateIngredient(graphene.Mutation):
    ingredient = graphene.Field(lambda: Ingredient, description="Inredient created by this mutation")

    class Arguments:
        input = CreateIngredientInput(required=True)

    @jwt_required
    def mutate(self, info, input):
        data = input_to_dictionary(input)

        ingredient = ModelIngredient(**data)
        db_session.add(ingredient)
        db_session.commit()
        return CreateIngredient(ingredient=ingredient)


class UpdateIngredientInput(graphene.InputObjectType, IngredientAttributes):
    id = graphene.ID(required=True, description="Global ID of the ingredient")


class UpdateIngredient(graphene.Mutation):
    ingredient = graphene.Field(lambda: Ingredient, description="Ingredient updated by this mutation")

    class Arguments:
        input = UpdateIngredientInput(required=True)

    @jwt_required
    def mutate(self, info, input):
        data = input_to_dictionary(input)

        ingredient = db_session.query(ModelIngredient).filter_by(id=data["id"])
        ingredient.update(data)
        db_session.commit()
        ingredient = db_session.query(ModelIngredient).filter_by(id=data["id"]).first()
        return UpdateIngredient(ingredient=ingredient)