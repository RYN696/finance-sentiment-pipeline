import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("NEWSAPI_KEY")

# Liste des entreprises à suivre (vous pourrez l'étendre plus tard)
ENTREPRISES = ["TotalEnergies", "LVMH", "Sanofi"]

url = "https://newsapi.org/v2/everything"
tous_les_articles = []

for entreprise in ENTREPRISES:
    params = {
        "q": f'"{entreprise}"',   # guillemets = recherche exacte, moins de bruit
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get("status") == "ok":
        print(f"{entreprise} : {data['totalResults']} articles trouvés")
        for article in data["articles"]:
            article["entreprise_cible"] = entreprise  # on garde une trace de la recherche
            tous_les_articles.append(article)
    else:
        print(f"Erreur pour {entreprise} :", data)

# Sauvegarde de tous les articles ensemble
os.makedirs("data", exist_ok=True)
with open("data/articles.json", "w", encoding="utf-8") as f:
    json.dump(tous_les_articles, f, ensure_ascii=False, indent=2)

print(f"\nTotal : {len(tous_les_articles)} articles sauvegardés dans data/articles.json")