from typing import Any, Optional
import requests

# Define the URL for adding and retrieving food item information
base_url = "http://localhost:8000/dishes"


def create_dish(name: str) -> int:
    # Make a POST request to add the food item
    response = requests.post(base_url, json={"name": name})
    return response.json() if response.status_code == 201 else -1

def get_dish(dish_id: int) -> Optional[dict[str, Any]]:
    # Make a GET request to retrieve the food item information
    get_url = f"{base_url}/{dish_id}"
    response = requests.get(get_url)
    return response.json() if response.status_code == 200 else {}

def get_dish_by_name(dish_name: str) -> Optional[dict[str, Any]]:
    # Make a GET request to retrieve the food item information
    get_url = f"{base_url}/{dish_name}"
    response = requests.get(get_url)
    return response.json() if response.status_code == 200 else None

def get_dish_details(dish_name:str) -> dict[str, Any]:
    if dish := get_dish_by_name(dish_name):
        return dish
    dish_id = create_dish(dish_name)
    return {} if dish_id < 0 else get_dish(dish_id)
    
def format_line(*_, **kwargs) -> str:
    if not kwargs:
        return ""
    return f'{kwargs["name"]} contains {kwargs["cal"]} calories, {kwargs["sodium"]} mgs of sodium, and {kwargs["sugar"]} grams of sugar\n'
# Read the queries from queries.txt and process each line
with open("queries.txt", "r") as queries_file:
    lines = queries_file.readlines()

response_lines = map(lambda line: format_line(**get_dish_details(line.strip())), lines)
# Write the response lines to response.txt
with open("response.txt", "w") as response_file:
    response_file.writelines(response_lines)