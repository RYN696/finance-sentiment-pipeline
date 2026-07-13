import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ALPHAVANTAGE_KEY")

# Liste des entreprises avec leurs tickers boursiers
ENTREPRISES = {
    "TotalEnergies": "TTE",
    "Sanofi": "SNY",
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    "Tesla": "TSLA",
    "Google": "GOOGL",
    "Meta": "META",
    "Nvidia": "NVDA",
    "JPMorgan": "JPM",
    "Johnson & Johnson": "JNJ",
    "Walmart": "WMT",
    "Visa": "V",
    "ExxonMobil": "XOM"
}

url = "https://www.alphavantage.co/query"
tous_les_articles = []

for entreprise, ticker in ENTREPRISES.items():
    params = {
        "function": "NEWS_SENTIMENT",
        "tickers": ticker,
        "limit": 200,
        "apikey": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "feed" in data:
        nb = len(data["feed"])
        print(f"{entreprise} ({ticker}) : {nb} articles récupérés")
        for article in data["feed"]:
            article["entreprise_cible"] = entreprise
            tous_les_articles.append(article)
    else:
        print(f"Erreur ou limite atteinte pour {entreprise} :", data.get("Information", data.get("Note", data)))

    time.sleep(12)  # Alpha Vantage limite à 5 requêtes/minute en gratuit

os.makedirs("data", exist_ok=True)
with open("data/articles_alphavantage.json", "w", encoding="utf-8") as f:
    json.dump(tous_les_articles, f, ensure_ascii=False, indent=2)

print(f"\nTotal : {len(tous_les_articles)} articles sauvegardés dans data/articles_alphavantage.json")