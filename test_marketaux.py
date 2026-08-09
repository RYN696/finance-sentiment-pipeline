import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("MARKETAUX_KEY")

url = "https://api.marketaux.com/v1/news/all"
params = {
    "symbols": "AAPL",
    "filter_entities": "true",
    "language": "en",
    "api_token": API_KEY
}

response = requests.get(url, params=params)
data = response.json()

print(json.dumps(data, indent=2, ensure_ascii=False)[:2000])