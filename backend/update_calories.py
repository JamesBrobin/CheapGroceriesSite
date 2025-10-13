import psycopg2
from estimate_calories_from_ai import estimate_calories_from_ai
import os
import psycopg2
from dotenv import load_dotenv
import upc_database_api  # Add this import to fix the undefined error

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

    cur.execute("SELECT id, upc, name, price, size FROM products WHERE calories_per_package IS NULL")

    products = cur.fetchall()
    
    for prod_id, upc, name, price, size in products:

        #calories_per_package = estimate_calories_from_ai(name, size)

        calories_per_package = upc_database_api.get_calories_from_upc(upc)

        print(calories_per_package)

        price_float = float(price) if price is not None else None

        # Convert to float safely
        if calories_per_package is not None:
            calories_per_package = float(calories_per_package)
        else:
            calories_per_package = None

        # Then divide
        if calories_per_package and price_float:
            calories_per_dollar = calories_per_package / price_float
        else:
            calories_per_dollar = None

        print(calories_per_dollar)
                    
        cur.execute("""
            UPDATE products
            SET calories_per_package=%s,
                calories_per_dollar=%s,
                ai_estimate=%s
                WHERE id=%s
        """, (calories_per_package, calories_per_dollar, "TRUE" if calories_per_package is not None else "FALSE", prod_id))

        
        
    
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    update_product_calories()