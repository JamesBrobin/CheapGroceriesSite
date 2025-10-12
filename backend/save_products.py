import psycopg2
from kroger_api import get_access_token, search_products
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")


def save_products_to_db(products):
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST
    )
    cur = conn.cursor()

    for item in products["data"]:
        name = item["description"]
        brand = item["brand"]
        upc = item["upc"]
        price_data = item.get("items", [{}])[0].get("price", {})
        price = price_data.get("regular")
        currency = "USD"

        cur.execute(
            "INSERT INTO products (name, brand, upc, price, currency) VALUES (%s, %s, %s, %s, %s)",
            (name, brand, upc, price, currency)
        )
    
    print("Number of products returned:", len(products.get("data", [])))

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    token = get_access_token()
    products = search_products("milk", token)
    save_products_to_db(products)
