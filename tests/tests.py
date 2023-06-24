import connectionController
from tests.assertions import assert_any_of_err_code, assert_err_code, assert_ret_value
from tests.restApiController import add_dish, add_meal

def get_dish_id(dish_name: str) -> int:
    response = connectionController.http_get(f"dishes/{dish_name}")
    if response.status_code == 404:
        return add_dish(dish_name)
    return response.json()["ID"]
        

# tests for dish API

def test_create_3_dishes():
    ids = {add_dish(dish_name['name']) for dish_name in ["orange", "spaghetti", "apple pie"]}
    assert len(ids) == 3
    
def test_get_orange():
    orange_id = get_dish_id("orange")
    response = connectionController.http_get(f"dishes/{orange_id}")
    assert response.status_code == 200
    assert 0.9<=response.json()["sodium"]<=1.1

def test_get_all_dishes():
    response = connectionController.http_get("dishes")
    assert_err_code(response, error_code=200)
    assert len(response.json()) == 3


def test_add_invalid_dish():
    INVALID_DISH = {"name": "blah"}
    response = connectionController.http_post("dishes", INVALID_DISH)
    assert_any_of_err_code(response,[422,404,400])
    assert_ret_value(response, -3)
    
def test_add_exists_dish():
    response = connectionController.http_get("dishes/orange")
    if response.status_code == 404:
        add_dish("orange")
    DISH_NAME = "orange"
    add_dish(DISH_NAME)
    response = connectionController.http_post("dishes", {"name": DISH_NAME})
    assert_any_of_err_code(response,[422,404,400])
    assert_ret_value(response, -2)


# tests for meals API


def test_meals_sanity():
    NO_MEALS = {}
    response = connectionController.http_get("meals")
    assert_err_code(response, error_code=200)
    assert_ret_value(response, NO_MEALS)


def add_first_meal():
    appetizer_id = get_dish_id("orange")
    main_id = get_dish_id("spaghetti")
    dessert_id = get_dish_id("apple pie")
    add_meal("delicious", appetizer_id, main_id, dessert_id)

def get_first_meal():
    response = connectionController.http_get("meals")
    meal_ids = response.json().keys()
    assert len(meal_ids) == 1
    meal = response.json().keys()[meal_ids[0]]
    assert 400 <= meal["calories"] <= 500

def test_add_exists_meal():
    meal = {"name": "test_add_exists_meal meal", "appetizer": 1, "main": 1, "dessert": 1}
    add_meal(meal["name"], meal["appetizer"], meal["main"], meal["dessert"])
    response = connectionController.http_post("meals", meal)
    assert_any_of_err_code(response,[422,400])
    assert_ret_value(response, returned_value=-2)