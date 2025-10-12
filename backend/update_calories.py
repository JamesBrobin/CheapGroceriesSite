import psycopg2
from kroger_api import get_access_token, search_products
from usda_api import get_calories_from_usda
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

def update_product_calories():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST
    )
    cur = conn.cursor()

    #cur.execute("SELECT id, name, price FROM products WHERE calories_per_package IS NULL")
    cur.execute("SELECT id, name, price FROM products")

    products = cur.fetchall()
    
    for prod_id, name, price in products:

        #print(name)

        calories_per_serving = get_calories_from_usda(name)
        if calories_per_serving is None:
            continue  # skip if no data
        
        servings_per_package = 1  # default to 1 if unknown
        calories_per_package = calories_per_serving * servings_per_package
        price_float = float(price) if price is not None else 0
        calories_per_dollar = calories_per_package / price_float if price_float else None

        #print(servings_per_package)
        #print(calories_per_package)
        #print(price)
        #print(calories_per_dollar)
        
        cur.execute("""
            UPDATE products
            SET calories_per_serving=%s,
                servings_per_package=%s,
                calories_per_package=%s,
                calories_per_dollar=%s
            WHERE id=%s
        """, (calories_per_serving, servings_per_package, calories_per_package, calories_per_dollar, prod_id))
    
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    update_product_calories()