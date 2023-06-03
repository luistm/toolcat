from pytest_bdd import given, scenarios, then, when  # type: ignore

scenarios("../makecake.feature")


@given("a random list of cake ingredients")
def given_a_random_list_of_cake_ingredients():
    pass


@when("a recipe is asked")
def a_recipe_is_asked():
    pass


@then("a recipe is provided")
def a_recipe_is_provided():
    pass
