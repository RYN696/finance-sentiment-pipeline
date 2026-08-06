import os
import json
import time
import requests
from dotenv import load_dotenv
import sys
from pathlib import Path

# Permet d'importer config.py depuis src/, peu importe d'où ce script est lancé
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import RAW_DIR, ARTICLES_ALPHAVANTAGE

load_dotenv()
API_KEY = os.getenv("ALPHAVANTAGE_KEY")

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
    "Johnson & Johnson": "JNJ"
}

def collecter():
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
            print(f"{entreprise} ({ticker}) : {len(data['feed'])} articles récupérés")
            for article in data["feed"]:
                article["entreprise_cible"] = entreprise
                tous_les_articles.append(article)
        else:
            print(f"Erreur pour {entreprise} :", data.get("Information", data.get("Note", data)))

        time.sleep(12)

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    with open(ARTICLES_ALPHAVANTAGE, "w", encoding="utf-8") as f:
        json.dump(tous_les_articles, f, ensure_ascii=False, indent=2)

    print(f"\nTotal : {len(tous_les_articles)} articles sauvegardés dans {ARTICLES_ALPHAVANTAGE}")

if __name__ == "__main__":
    collecter()