from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os
import requests
from dotenv import load_dotenv
import pprint

app = FastAPI(
    title="UPC Product Lookup API",
    description="Fetch product information from the UPC Database API",
    version="1.0.0"
)

load_dotenv()
API_KEY = os.getenv("UPC_API_KEY")
BASE_URL = "https://api.upcdatabase.org/product"


def clean_upc(upc: str) -> str:
    """Remove non-digit characters from UPC."""
    return ''.join(filter(str.isdigit, upc))

def generate_upc_variants(upc: str):
    """
    Generate likely UPC formats to increase chance of a match.
    UPC-A: 12 digits
    EAN-13: 13 digits
    """
    upc = clean_upc(upc)
    variants = set()

    # Original UPC
    variants.add(upc)

    # Pad with leading zeros
    if len(upc) < 12:
        variants.add(upc.zfill(12))  # UPC-A
    if len(upc) < 13:
        variants.add(upc.zfill(13))  # EAN-13

    # Trim to 12 or 13 if too long
    if len(upc) > 12:
        variants.add(upc[-12:])
    if len(upc) > 13:
        variants.add(upc[-13:])

    return list(variants)

def get_calories_from_upc(upc: str):

    print("Looking up UPC:", upc)

    variants = generate_upc_variants(upc)

    for variant in variants:
        print("Trying variant:", variant)
        product = lookup_product(variant)
        print("Product data:", product)


    return product.get('metanutrition', {}).get('energy-kcal')

def lookup_product(upc: str):
    url = f"{BASE_URL}/{upc}?apikey={API_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

@app.get("/lookup/{upc}")
def get_product(upc: str):
    try:
        data = lookup_product(upc)
        return JSONResponse(content=data)
    except requests.HTTPError as e:
        try:
            error_data = e.response.json()
        except Exception:
            error_data = {"error": str(e)}
        return JSONResponse(content=error_data, status_code=e.response.status_code)

if __name__ == "__main__":
    info = lookup_product("4600013755")  # Example UPC for testing
    energy_kcal = info.get('metanutrition', {}).get('energy-kcal')
    
    pprint.pprint(info)

    print("Calories (kcal):", energy_kcal)
