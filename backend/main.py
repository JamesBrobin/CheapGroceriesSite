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
                cur.execute("SELECT name, brand, price FROM products LIMIT 10;")
                rows = cur.fetchall()
                return [
                    {"name": r[0], "brand": r[1], "price": float(r[2]) if r[2] else None} 
                    for r in rows
                ]
    except OperationalError as e:
        return {"error": "Database connection failed", "details": str(e)}