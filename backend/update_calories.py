import psycopg2
from estimate_calories_from_ai import estimate_calories_from_ai
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

    cur.execute("SELECT id, name, price FROM products WHERE calories_per_package IS NULL")

    products = cur.fetchall()
    
    for prod_id, name, price in products:

        calories_per_package = estimate_calories_from_ai(name)

        try:
            price_float = float(price) if price is not None else None
        except ValueError:
            continue

    
        calories_per_dollar = calories_per_package / price_float if price_float else None
        
        cur.execute("""
            UPDATE products
            SET calories_per_serving=%s,
                servings_per_package=%s,
                calories_per_package=%s,
                calories_per_dollar=%s
            WHERE id=%s
        """, ("0", "0", calories_per_package, calories_per_dollar, prod_id))
    
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    update_product_calories()