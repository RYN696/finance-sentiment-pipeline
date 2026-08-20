import os
import json
import time
import requests
from dotenv import load_dotenv
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import RAW_DIR, ARTICLES_ALPHAVANTAGE


load_dotenv()

API_KEY = os.getenv("ALPHAVANTAGE_KEY")

# Nombre maximum d'articles conservés PAR entreprise
MAX_ARTICLES_PAR_ENTREPRISE = 20

# Pause entre les requêtes
TEMPS_ATTENTE = 12


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



# COLLECTE DES ARTICLES

def collecter():

    if not API_KEY:
        print("ERREUR : la clé ALPHAVANTAGE_KEY est introuvable.")
        print("Vérifie ton fichier .env")
        return

    url = "https://www.alphavantage.co/query"

    tous_les_articles = []

    print("DÉBUT DE LA COLLECTE")


    for entreprise, ticker in ENTREPRISES.items():

        print(f"\nRecherche des articles pour {entreprise} ({ticker})...")

        params = {
            "function": "NEWS_SENTIMENT",
            "tickers": ticker,
            "limit": 50,
            "apikey": API_KEY
        }

        try:
            response = requests.get(
                url,
                params=params,
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

        except requests.exceptions.RequestException as e:
            print(f"Erreur réseau pour {entreprise} : {e}")
            continue

        except ValueError:
            print(f"Erreur : réponse JSON invalide pour {entreprise}")
            continue

        if "feed" in data:

            articles = data["feed"][:MAX_ARTICLES_PAR_ENTREPRISE]

            print(
                f"{entreprise} ({ticker}) : "
                f"{len(data['feed'])} reçus → "
                f"{len(articles)} conservés"
            )

            # Ajouter le nom de l'entreprise
            for article in articles:

                article["entreprise_cible"] = entreprise
                article["ticker_cible"] = ticker

                tous_les_articles.append(article)

        else:

            print(
                f"Erreur pour {entreprise} : "
                f"{data.get('Information', data.get('Note', data))}"
            )

        # Attente pour respecter les limites de l'API
        print(f"Attente de {TEMPS_ATTENTE} secondes...")
        time.sleep(TEMPS_ATTENTE)


    RAW_DIR.mkdir(parents=True, exist_ok=True)

    with open(
        ARTICLES_ALPHAVANTAGE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            tous_les_articles,
            f,
            ensure_ascii=False,
            indent=2
        )


    print("\n" + "=" * 60)
    print("COLLECTE TERMINÉE")
    print("=" * 60)

    print(
        f"Total : {len(tous_les_articles)} articles sauvegardés"
    )

    print(
        f"Fichier : {ARTICLES_ALPHAVANTAGE}"
    )


if __name__ == "__main__":
    collecter()