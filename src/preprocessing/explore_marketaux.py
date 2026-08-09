import json
import sys
from pathlib import Path
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import RAW_DIR

with open(RAW_DIR / "articles_marketaux.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

df = pd.DataFrame(articles)

print(f"Nombre total d'articles : {len(df)}")

print("\nRépartition par entreprise :")
print(df["entreprise_cible"].value_counts())

print("\nStatistiques du match_score :")
print(df["match_score"].describe())

print("\nArticles avec match_score faible (< 5, potentiellement peu pertinents) :")
faibles = df[df["match_score"] < 5]
print(f"{len(faibles)} articles")
print(faibles[["entreprise_cible", "title", "match_score"]])

print("\nArticles avec summary vide ou très court :")
courts = df[df["summary"].fillna("").str.len() < 50]
print(f"{len(courts)} articles")

doublons = df.duplicated(subset=["title"]).sum()
print(f"\nDoublons détectés : {doublons}")

# Nettoyage léger : retirer doublons, summary vides, et match_score très faible
df_propre = df.drop_duplicates(subset=["title"])
df_propre = df_propre[df_propre["summary"].fillna("").str.len() >= 50]
df_propre = df_propre[df_propre["match_score"] >= 5]

print(f"\nAprès nettoyage : {len(df_propre)} articles (sur {len(df)} au départ)")

from config import PROCESSED_DIR
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
df_propre.to_json(PROCESSED_DIR / "marketaux_prepares.json", orient="records", force_ascii=False, indent=2)
print(f"Sauvegardé dans {PROCESSED_DIR / 'marketaux_prepares.json'}")