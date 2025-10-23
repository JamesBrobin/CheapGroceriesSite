import psycopg2
from test_usda_api import get_calories_from_usda
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

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

def update_product_calories():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST
    )
    cur = conn.cursor()

    # cur.execute("SELECT id, upc, name, price, size_from_kroger FROM products WHERE calories_per_package IS NULL")
    cur.execute("SELECT id, upc, name, price, size_from_kroger FROM products")


    products = cur.fetchall()
    
    for prod_id, upc, name, price, size_from_kroger in products:

        #calories_per_package = estimate_calories_from_ai(name, size)

        #calories_per_package = upc_database_api.get_calories_from_upc(upc)

        calories_per_100_grams, usda_description = get_calories_from_usda(name)

        source = "USDA"

        size_in_grams = size_to_grams(size_from_kroger) if size_from_kroger else None

        calories_per_package = None

        if calories_per_100_grams and size_in_grams:
            calories_per_package = calories_per_100_grams * (size_in_grams / 100)

        price_float = None

        if price is not None:
            price_float = float(price)

        if calories_per_package and price_float:
            calories_per_dollar = calories_per_package / price_float
        else:
            calories_per_dollar = None

        print("Product: ", name)
        print("USDA Description: ", usda_description)
        print("Size from kroger: ", size_from_kroger)
        print("Size in grams: ", size_in_grams)
        print("Calories per 100g: ", calories_per_100_grams)
        print("Calories per package: ", calories_per_package)
        print("Price: ", price)
        print("Calories per dollar: ", calories_per_dollar)
                    
        cur.execute("""
            UPDATE products
            SET usda_description=%s,
                size_from_kroger=%s,
                size_in_grams=%s,
                calories_per_package=%s,
                calories_per_100_grams=%s,
                calories_per_dollar=%s,
                source=%s
                WHERE id=%s
        """, (usda_description, size_from_kroger, size_in_grams, calories_per_package, calories_per_100_grams, calories_per_dollar, source, prod_id))

        
        
    
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    update_product_calories()