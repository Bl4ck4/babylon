try:
    from .recipe import Recipe
except AssertionError:
    pass
from .measured_in import MeasuredIn
from .ingredient import Ingredient
from .tag import Tag
