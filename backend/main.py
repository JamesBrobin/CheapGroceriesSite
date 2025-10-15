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
                        upc,
                        name,
                        usda_description,
                        brand,
                        price,
                        currency,
                        size_from_kroger,
                        size_in_grams,
                        calories_per_package,
                        calories_per_100_grams,
                        calories_per_dollar,
                        ai_estimate
                    FROM products
                    ORDER BY calories_per_dollar DESC NULLS LAST;
                """)
                rows = cur.fetchall()
                return [
                    {
                        "upc": r[0],
                        "name": r[1],
                        "usda_description": r[2],
                        "brand": r[3],
                        "price": float(r[4]) if r[4] is not None else None,
                        "currency": r[5],
                        "size_from_kroger": r[6],
                        "size_in_grams": float(r[7]) if r[7] is not None else None,
                        "calories_per_package": float(r[8]) if r[8] is not None else None,
                        "calories_per_100_grams": float(r[9]) if r[9] is not None else None,
                        "calories_per_dollar": float(r[10]) if r[10] is not None else None,
                        "ai_estimate": bool(r[11]) if r[11] is not None else False
                    }
                    for r in rows
                ]
    except OperationalError as e:
        return {"error": "Database connection failed", "details": str(e)}
