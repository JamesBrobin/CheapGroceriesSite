import psycopg2
from kroger_api import get_access_token, search_products
from dotenv import load_dotenv
import os
import json

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
        size_from_kroger = item.get("items", [{}])[0].get("size")
        currency = "USD"

        print(name)
        print(price)
        print(size_from_kroger)

        print(json.dumps(item, indent=2))

        cur.execute("""
            INSERT INTO products (
                upc, name, brand, price, currency, size_from_kroger
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (upc) DO UPDATE SET
                upc = EXCLUDED.upc,
                name = EXCLUDED.name,
                brand = EXCLUDED.brand,
                price = EXCLUDED.price,
                currency = EXCLUDED.currency,
                size_from_kroger = EXCLUDED.size_from_kroger
        """, (
            upc,
            name,
            brand,
            price,
            currency,
            size_from_kroger
        ))

    
    print("Number of products returned:", len(products.get("data", [])))

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    token = get_access_token()
    products = search_products("dried black beans", token)
    save_products_to_db(products)
