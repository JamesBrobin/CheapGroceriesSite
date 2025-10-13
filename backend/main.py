from fastapi import FastAPI
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

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


from psycopg2 import OperationalError

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
                        SELECT name, brand, price, size, calories_per_package, calories_per_dollar
                        FROM products;
                    """) 
                rows = cur.fetchall()
                return [
                            {
                                "name": r[0],
                                "brand": r[1],
                                "price": float(r[2]) if r[2] else None,
                                "size": r[3],
                                "calories_per_package": float(r[4]) if r[4] else None,
                                "calories_per_dollar": float(r[5]) if r[5] else None
                            } for r in rows
                        ]
    except OperationalError as e:
        return {"error": "Database connection failed", "details": str(e)}