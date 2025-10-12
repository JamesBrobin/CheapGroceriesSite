import requests
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
USDA_API_KEY = os.getenv("USDA_API_KEY")

def search_food(food_name):
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {
        "api_key": USDA_API_KEY,
        "query": food_name,
        "pageSize": 3  # just get top 3 results
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data

if __name__ == "__main__":
    food_name = "banana"  # change this to anything you want
    result = search_food(food_name)
    import json
    print(json.dumps(result, indent=2))
