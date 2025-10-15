import requests
import pprint

# ------------------------------
# CONFIG
# ------------------------------
FDC_API_KEY = "VQphXh7JT5AqV2kAWQaQ5KlxBz4bniUxF1MMZzMq"  # Replace with your USDA API key

# Example product JSON
KROGER_JSON = {
    "items": [{"price": {"regular": 1.89}, "size": "16 oz"}],
    "description": "Kroger Black Beans"
}

# ------------------------------
# FUNCTIONS
# ------------------------------

def size_to_grams(size_str):
    size_str = size_str.lower().strip()
    if "oz" in size_str:
        number = float(size_str.replace("oz", "").strip())
        return number * 28.3495
    elif "lb" in size_str:
        number = float(size_str.replace("lb", "").strip())
        return number * 453.592
    elif "g" in size_str:
        return float(size_str.replace("g", "").strip())
    elif "kg" in size_str:
        return float(size_str.replace("kg", "").strip()) * 1000
    else:
        raise ValueError(f"Unknown size unit in '{size_str}'")

def search_fdс(description):
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {
        "api_key": FDC_API_KEY,
        "query": description,
        "pageSize": 1
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data.get("foods"):
        return data["foods"][0]["fdcId"]
    else:
        raise ValueError("No USDA food found for description")

def get_calories_per_100g(fdc_id):
    url = f"https://api.nal.usda.gov/fdc/v1/food/{fdc_id}"
    params = {"api_key": FDC_API_KEY}
    response = requests.get(url, params=params)
    data = response.json()

    pprint.pprint(data)  # Debugging line to inspect the data structure

    for nutrient in data.get("foodNutrients", []):
        name = nutrient.get("nutrientName")
        unit = nutrient.get("unitName")
        if name and unit:  # make sure both exist
            if name.lower() == "energy" and unit.upper() == "KCAL":
                return nutrient["value"]
    
    raise ValueError("Calories not found in USDA data")

def calories_per_dollar(cal_per_100g, package_size_oz, price):
    grams = size_to_grams(package_size_oz)
    total_calories = cal_per_100g * (grams / 100)
    return total_calories / price

# ------------------------------
# MAIN FUNCTION
# ------------------------------

def main(product_json):
    description = product_json["description"]
    price = product_json["items"][0]["price"]["regular"]
    package_size = product_json["items"][0]["size"]

    fdc_id = search_fdс(description)
    cal_per_100g = get_calories_per_100g(fdc_id)
    cpd = calories_per_dollar(cal_per_100g, package_size, price)
    print(f"Calories per dollar for '{description}': {cpd:.2f} kcal/$")
    return cpd

# ------------------------------
# RUN SCRIPT
# ------------------------------

if __name__ == "__main__":
    main(KROGER_JSON)
