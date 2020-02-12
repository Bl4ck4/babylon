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
        return [ingredient.ingredient for ingredient in self.ingredients]

    class Meta:
        model = ModelFridge
        interfaces = (graphene.relay.Node,)


'''
class CreateRecipeInput(graphene.InputObjectType, FridgeAttributes):
    pass

class CreateRecipe(graphene.Mutation):
    recipe = graphene.Field(lambda: Fridge, description="Recipe created by this mutation")

    class Arguments:
        input = CreateRecipeInput(required=True)

    @jwt_required
    def mutate(self, info, input):
        data = input
        tags = data.pop("tag_id")
        ingredients = data.pop("ingredient_id")

        recipe = ModelRecipe(**data)
        for tag_id in tags:
            recipe.tags.append(db_session.query(ModelTag).filter(ModelTag.name == tag_id).first())
        for ingredient_id in ingredients:
            ingredient = db_session.query(ModelIngredient).filter(ModelIngredient.name == ingredient_id).first()
            recipe.ingredients.append(
                db_session.query(IngredientAssociation).filter(IngredientAssociation.ingredient_id == ingredient.id).first()
            )

        db_session.add(recipe)
        db_session.commit()
        return CreateRecipe(recipe=recipe)


class UpdateRecipeInput(graphene.InputObjectType, RecipeAttributes):
    id = graphene.ID(required=True, description="Global ID of the recipe")


class UpdateRecipe(graphene.Mutation):
    recipe = graphene.Field(lambda: Recipe, description="Recipe created by this mutation")

    class Arguments:
        input = CreateRecipeInput(required=True)

    @jwt_required
    def mutate(self, info, input):
        data = input_to_dictionary(input)

        recipe = db_session.query(ModelRecipe).filter_by(id=data["id"])
        recipe.update(data)
        db_session.commit()
        recipe = db_session.query(ModelRecipe).filter_by(id=data["id"]).first()
        return UpdateRecipe(recipe=recipe)
'''