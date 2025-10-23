from fastapi import FastAPI
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2 import OperationalError
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

app = FastAPI()

# Allow frontend access (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}


@app.get("/products")
def get_products():
    try:
        with psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        id,
                        upc,
                        store,
                        zipcode,
                        name,
                        brand,
                        usda_description,
                        price,
                        currency,
                        size_from_kroger,
                        size_in_grams,
                        calories_per_100_grams,
                        calories_per_package,
                        calories_per_dollar,
                        source
                    FROM products
                    ORDER BY calories_per_dollar DESC NULLS LAST;
                """)
                rows = cur.fetchall()

                return [
                    {
                        "id": r[0],
                        "upc": r[1],
                        "store": r[2],
                        "zipcode": r[3],
                        "name": r[4],
                        "brand": r[5],
                        "usda_description": r[6],
                        "price": float(r[7]) if r[7] is not None else None,
                        "currency": r[8],
                        "size_from_kroger": r[9],
                        "size_in_grams": float(r[10]) if r[10] is not None else None,
                        "calories_per_100_grams": float(r[11]) if r[11] is not None else None,
                        "calories_per_package": float(r[12]) if r[12] is not None else None,
                        "calories_per_dollar": float(r[13]) if r[13] is not None else None,
                        "source": r[14],
                    }
                    for r in rows
                ]

    except OperationalError as e:
        return {"error": "Database connection failed", "details": str(e)}
    except Exception as e:
        # General fallback for SQL or parsing errors
        return {"error": "Unexpected error", "details": str(e)}