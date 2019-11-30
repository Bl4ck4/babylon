from graphene_sqlalchemy import SQLAlchemyConnectionField
import graphene
from . import Recipe, Ingredient, Tag, MeasuredIn

class Query(graphene.ObjectType):
    """Query objects for GraphQL API."""

    node = graphene.relay.Node.Field()
    recipe = graphene.relay.Node.Field(Recipe)
    recipeList = SQLAlchemyConnectionField(Recipe)
    ingredient = graphene.relay.Node.Field(Ingredient)
    ingredientList = SQLAlchemyConnectionField(Ingredient)
    tag = graphene.relay.Node.Field(Tag)
    tagList = SQLAlchemyConnectionField(Tag)
    measuredIn = graphene.relay.Node.Field(MeasuredIn)
    measuredInList = SQLAlchemyConnectionField(MeasuredIn)