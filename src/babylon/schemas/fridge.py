from graphene_sqlalchemy import SQLAlchemyObjectType
import graphene
from ..database import db_session
from ..models import ModelFridge
from ..lib.utils import input_to_dictionary
from importlib import import_module
from flask_jwt_extended import jwt_required


class FridgeAttributes:

    ingredient_id = graphene.List(graphene.String)


class Fridge(SQLAlchemyObjectType, FridgeAttributes):

    ingredients = graphene.List(lambda: import_module('.ingredient', "babylon.schemas").Ingredient)

    @graphene.resolve_only_args
    def resolve_ingredients(self):
        return [ingredient for ingredient in self.ingredients]

    class Meta:
        model = ModelFridge
        interfaces = (graphene.relay.Node,)


class CreateFridgeInput(graphene.InputObjectType, FridgeAttributes):
    pass


class CreateFridge(graphene.Mutation):
    recipe = graphene.Field(lambda: Fridge, description="Recipe created by this mutation")

    class Arguments:
        input = CreateFridgeInput(required=True)

    @jwt_required
    def mutate(self, info, input):
        # TODO: Add this
        pass


class UpdateFridgeInput(graphene.InputObjectType, FridgeAttributes):
    id = graphene.ID(required=True, description="Global ID of the recipe")


class UpdateFridge(graphene.Mutation):
    recipe = graphene.Field(lambda: Fridge, description="Recipe created by this mutation")

    class Arguments:
        input = CreateFridgeInput(required=True)

    @jwt_required
    def mutate(self, info, input):
        data = input_to_dictionary(input)

        fridge = db_session.query(ModelFridge).filter_by(id=data["id"])
        fridge.update(data)
        db_session.commit()
        recipe = db_session.query(ModelFridge).filter_by(id=data["id"]).first()
        return UpdateFridge(recipe=recipe)