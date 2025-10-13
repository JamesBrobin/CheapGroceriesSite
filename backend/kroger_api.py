import requests
import os
from dotenv import load_dotenv

load_dotenv()

KROGER_CLIENT_ID = os.getenv("KROGER_CLIENT_ID")
KROGER_CLIENT_SECRET = os.getenv("KROGER_CLIENT_SECRET")

def get_access_token():
    url = "https://api.kroger.com/v1/connect/oauth2/token"
    data = {
        "grant_type": "client_credentials",
        "scope": "product.compact"
    }
    auth = (KROGER_CLIENT_ID, KROGER_CLIENT_SECRET)
    response = requests.post(url, data=data, auth=auth)
    response.raise_for_status()
    token = response.json()["access_token"]
    return token

def search_products(query, token, limit=50):
    url = f"https://api.kroger.com/v1/products?filter.term={query}&filter.limit={limit}&filter.locationId=01400943"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    token = get_access_token()
    products = search_products("beans", token)
    print(products)

