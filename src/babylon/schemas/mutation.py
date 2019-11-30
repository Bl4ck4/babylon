import graphene
from .tag import CreateTag, UpdateTag
from .ingredient import CreateIngredient, UpdateIngredient
from .measured_in import CreateMeasuredIn, UpdateMeasuredIn
from .recipe import CreateRecipe, UpdateRecipe


class Mutation(graphene.ObjectType):
    createTag = CreateTag.Field()
    updateTag = UpdateTag.Field()
    createIngredient = CreateIngredient.Field()
    updateIngredient = UpdateIngredient.Field()
    createMeasuredIn = CreateMeasuredIn.Field()
    updateMeasuredIn = UpdateMeasuredIn.Field()
    createRecipe = CreateRecipe.Field()
    updateRecipe = UpdateRecipe.Field()