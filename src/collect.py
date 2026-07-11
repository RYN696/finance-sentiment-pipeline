import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("NEWSAPI_KEY")

# Liste large d'entreprises cotées (CAC40 + quelques grandes internationales)
ENTREPRISES = [
    "TotalEnergies", "LVMH", "Sanofi", "L'Oreal", "Air Liquide",
    "Schneider Electric", "BNP Paribas", "AXA", "Danone", "Airbus",
    "Kering", "Michelin", "Renault", "Orange", "Vinci",
    "Carrefour", "Société Générale", "Saint-Gobain", "Capgemini", "Publicis",
    "Apple", "Microsoft", "Amazon", "Tesla", "Google"
]

url = "https://newsapi.org/v2/everything"
tous_les_articles = []

for entreprise in ENTREPRISES:
    params = {
        "q": f'"{entreprise}"',
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 100,   # maximum autorisé par requête
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get("status") == "ok":
        nb = len(data["articles"])
        print(f"{entreprise} : {nb} articles récupérés")
        for article in data["articles"]:
            article["entreprise_cible"] = entreprise
            tous_les_articles.append(article)
    else:
        print(f"Erreur pour {entreprise} :", data.get("message", data))

    time.sleep(1)  # petite pause pour ne pas surcharger l'API

# Sauvegarde de tous les articles
os.makedirs("data", exist_ok=True)
with open("data/articles.json", "w", encoding="utf-8") as f:
    json.dump(tous_les_articles, f, ensure_ascii=False, indent=2)

print(f"\nTotal : {len(tous_les_articles)} articles sauvegardés dans data/articles.json")