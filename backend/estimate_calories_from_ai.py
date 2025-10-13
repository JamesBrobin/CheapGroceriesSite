import os
import openai
from dotenv import load_dotenv
import requests
import json

load_dotenv()
openai.api_key = os.getenv("OPEN_ROUTER_API_KEY")

def estimate_calories_from_ai(product_name, size):
    prompt = f"""
    You are a nutrition assistant. Estimate the total calories in this product: "{product_name}".
    It's size is: "{size}".
    Return only a number.
    """

    response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": "Bearer " + openai.api_key,
  },
  data=json.dumps({
    "model": "deepseek/deepseek-chat-v3.1", # Optional
    "messages": [
      {
        "role": "user",
        "content": prompt
      }
    ]
  })
)
    text = response.json().get("choices")[0].get("message").get("content")
    print(text)
    try:
        calories = float(text)
        return calories
    except ValueError:
        return None