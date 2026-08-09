import os
import json
import time
import requests
import sys
from pathlib import Path
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import RAW_DIR

load_dotenv()
API_KEY = os.getenv("MARKETAUX_KEY")

ENTREPRISES = {
    "TotalEnergies": "TTE", "LVMH": "MC", "Sanofi": "SNY",
    "Air Liquide": "AI", "Schneider Electric": "SU", "BNP Paribas": "BNP",
    "AXA": "CS", "Danone": "BN", "Airbus": "AIR",
    "Apple": "AAPL", "Microsoft": "MSFT", "Amazon": "AMZN",
    "Tesla": "TSLA", "Google": "GOOGL", "Meta": "META",
    "Nvidia": "NVDA", "JPMorgan": "JPM", "Johnson & Johnson": "JNJ",
    "Walmart": "WMT", "Visa": "V", "ExxonMobil": "XOM",
    "Coca-Cola": "KO", "Netflix": "NFLX", "Disney": "DIS", "Intel": "INTC"
}

def collecter():
    url = "https://api.marketaux.com/v1/news/all"
    
    # Charger les articles déjà existants, s'il y en a
    output_path = RAW_DIR / "articles_marketaux.json"
    if output_path.exists():
        with open(output_path, "r", encoding="utf-8") as f:
            tous_les_articles = json.load(f)
    else:
        tous_les_articles = []

    urls_existantes = {a["url"] for a in tous_les_articles}  # évite les doublons

    for entreprise, symbol in ENTREPRISES.items():
        params = {
            "symbols": symbol,
            "filter_entities": "true",
            "language": "en",
            "limit": 50,
            "api_token": API_KEY
        }

        response = requests.get(url, params=params)
        data = response.json()

        if "data" in data:
            print(f"{entreprise} ({symbol}) : {len(data['data'])} articles récupérés")
            for article in data["data"]:
                if article["url"] in urls_existantes:
                    continue  # déjà présent, on saute
                
                entite = next((e for e in article["entities"] if e["symbol"] == symbol), None)
                tous_les_articles.append({
                    "entreprise_cible": entreprise,
                    "title": article["title"],
                    "summary": article["description"],
                    "source": article["source"],
                    "url": article["url"],
                    "published_at": article["published_at"],
                    "match_score": entite["match_score"] if entite else None,
                    "marketaux_sentiment": entite["sentiment_score"] if entite else None
                })
                urls_existantes.add(article["url"])
        else:
            print(f"Erreur pour {entreprise} :", data)

        time.sleep(1)

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(tous_les_articles, f, ensure_ascii=False, indent=2)

    print(f"\nTotal cumulé : {len(tous_les_articles)} articles sauvegardés dans {output_path}")
    return tous_les_articles

if __name__ == "__main__":
    collecter()