from .ingredient import ModelIngredient
from .measured_in import ModelMeasuredIn
from .recipe import ModelRecipe, IngredientAssociation
from .tag import ModelTag
from .auth import User
from sqlalchemy import exists


def __init_korvgratang(db_session):
    liter = db_session.query(ModelMeasuredIn).filter(ModelMeasuredIn.measurement=="l").first()
    kilo = db_session.query(ModelMeasuredIn).filter(ModelMeasuredIn.measurement == "kg").first()
    dinner = db_session.query(ModelTag).filter(ModelTag.name == "dinner").first()
    ingredients = __add_ingredients(db_session, ("broccoli", 0.500, kilo),
                                    ("falusausage", 0.800, kilo),
                                    ("grated_cheese", 0.125, kilo),
                                    ("flour", 0.015, liter),
                                    ("cream", 0.1, liter),
                                    ("milk", 0.4, liter),
                                    ("white_pepper", 0.001, liter))
    recipe = ModelRecipe(
        "Korvgratäng",
        ("Put oven on 250c. Cut Broccoli to smaller pieces\n"
         "Boil water with salt and boil the broccoli a couple of minutes. Put broccoli in an oven pan.\n"
         "Cut the falusausage into smaller pieces. Put them on top of the broccoli.\n"
         "Measure flour and pour cream on it. Whisk it smooth.\n"
         "Whisk milk into the flour/cream mix and let boil whilst stirring. Reduce the heat and let boil for 1-2 minutes.\n"
         "Add cheese while stirring the mix until it melts."
         "Add salt and pepper.\n"
         "Pour the cheese sauce on the broccoli and falusausage\n"
         "Put into oven at 250C for about 10 minutes\n"
         "Serve with boiled rice, bulgur or pasta."),
        ("Korvgratäng is a tasty and simple recipe with falusausage, broccoli and a simple cheese sauce."
         " Cheese sauce can be purchased if you want to save time, but tastes better when homemade."),
        "Tobias Persson",
        5
    )
    for ingredient in ingredients.values():
        recipe.ingredients.append(ingredient)
    recipe.tags.append(dinner)
    __add_and_commit(db_session, recipe, *list(ingredients.values()))
    db_session.commit()


def __init_fiskfile(db_session):
    liter = db_session.query(ModelMeasuredIn).filter(ModelMeasuredIn.measurement=="l").first()
    kilo = db_session.query(ModelMeasuredIn).filter(ModelMeasuredIn.measurement == "kg").first()
    amount = db_session.query(ModelMeasuredIn).filter(ModelMeasuredIn.measurement == "st").first()

    dinner = db_session.query(ModelTag).filter(ModelTag.name == "dinner").first()

    ingredients = __add_ingredients(
        db_session,
        ("oil", 0.015, liter),
        ("white_fish", 1, kilo),
        ("tomato", 2, amount),
        ("paprika", 2, amount),
        ("coconut_milk", 0.400, kilo),
        ("salt", 0.005, kilo),
        ("fish_bouillon", 0.015, liter),
        ("lime", 0.030, liter),
        ("white_pepper", 0.001, liter)
    )

    recipe = ModelRecipe(
        "Ugnsbakad fiskfile i kokossås",
        ("Oil an oven pan.\n"
         "Add the fish.\n"
         "Cut paprika and tomato and add on top of the fish.\n"
         "Mix coconut milk with fish bouillon, lime and spices.\n"
         "Pour cocounut milk mix over the fish.\n"
         "Put into oven for 25 minutes."),
        ("Very good fish dish baked in the oven. An easy recipe with white fish, coconut milk, tomato and paprika."
         "Cooks easily in the oven and creates many portions. Possible to vary the dish with different vegetables."),
        "Tobias Persson",
        8
    )
    for ingredient in ingredients.values():
        recipe.ingredients.append(ingredient)
    recipe.tags.append(dinner)
    __add_and_commit(db_session, recipe, *list(ingredients.values()))
    db_session.commit()

def __add_and_commit(db_session, *items):
    [db_session.add(item) for item in items]
    return items


def __create(model, *items):
    return [model(*item) for item in items]


def __add_measurements(db_session, *measurements):
    return {measurement.measurement: measurement for measurement in
            __add_and_commit(db_session, *__create(ModelMeasuredIn, *measurements))}


def __add_ingredients(db_session, *ingredients):
    ingredient_dict = {}
    created_ingredients = []
    for ingredient in ingredients:
        name, amount, measured_in = ingredient
        (ret, ), = db_session.query(exists().where(ModelIngredient.name==name))
        if not ret:
            ingredient = __add_and_commit(db_session, *__create(ModelIngredient, (name,)))[0]
        else:
            ingredient = db_session.query(ModelIngredient).filter(ModelIngredient.name == name).first()
        created_ingredients.append((ingredient, name, amount, measured_in))

    for ingredient, name, amount, measured_in in created_ingredients:
        assoc = IngredientAssociation(amount=amount)
        assoc.ingredient = ingredient
        assoc.measured_in = measured_in
        ingredient_dict[name] = assoc
    return ingredient_dict


def __add_tags(db_session, *tags):
    return {tag.name: tag for tag in
            __add_and_commit(db_session, *__create(ModelTag, *tags))}


def init_db():

    import os
    from ..database import db_session, engine, db_path
    from ..database import Base
    if os.path.exists(db_path):
        os.remove(db_path)
    Base.metadata.create_all(engine)

    measurements = __add_measurements(db_session, ("kg",), ("l",), ("st",))
    kilo = measurements.get("kg")
    liter = measurements.get("l")

    tags = __add_tags(db_session, ("vegetarian",), ("boss",), ("dinner",))
    boss = tags.get("boss")

    __init_korvgratang(db_session)
    __init_fiskfile(db_session)

    ingredients = __add_ingredients(db_session, ("tomato", 1, kilo), ("beef", 5, kilo), ("milk", 20, liter))

    tomat = ingredients.get("tomato")
    biff = ingredients.get("beef")
    molk = ingredients.get("milk")

    receptet = ModelRecipe(
        "Something",
        "Put beef and tomato in pan\nPour milk.",
        "This is a description of the recipe",
        "Receptias",
        1
    )
    receptet.ingredients.append(tomat)
    receptet.ingredients.append(biff)
    receptet.ingredients.append(molk)
    receptet.tags.append(boss)

    __add_and_commit(db_session, receptet, *list(ingredients.values()))

    user = User("steve@internet.com", "mittpasswurd", True)
    __add_and_commit(db_session, user)

    db_session.commit()
