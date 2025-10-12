# main.py
from fastapi import FastAPI

# Create the FastAPI instance (this is what uvicorn looks for)
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
