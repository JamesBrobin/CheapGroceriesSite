import requests
import os
from dotenv import load_dotenv

load_dotenv()
USDA_API_KEY = os.getenv("USDA_API_KEY")

def get_calories_from_usda(product_name):
    """
    Search USDA FoodData Central for calories.
    Returns calories per 100g or per serving if available.
    """
    print(product_name);
    search_url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {
        "api_key": USDA_API_KEY,
        "query": product_name,
        "pageSize": 1
    }
    response = requests.get(search_url, params=params)
    response.raise_for_status()
    data = response.json()
    if data.get("foods"):
        food = data["foods"][0]
        # Look for energy in kcal in nutrients
        for nutrient in food.get("foodNutrients", []):
            if nutrient.get("nutrientName") == "Energy" and nutrient.get("unitName") == "KCAL":
                return nutrient.get("value")  # calories per 100g/serving
    return None
