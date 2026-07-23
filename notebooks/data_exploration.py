import json
import pandas as pd

with open("data/articles_alphavantage.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

df = pd.DataFrame(articles)

print("Nombre total d'articles :", len(df))
print("\nColonnes disponibles :", list(df.columns))

print("\nRépartition par entreprise :")
print(df["entreprise_cible"].value_counts())

print("\nAperçu d'un article complet (le premier) :")
print(json.dumps(articles[0], indent=2, ensure_ascii=False)[:1500])

doublons = df.duplicated(subset=["title"]).sum()
print(f"\nNombre de doublons détectés : {doublons}")

print("\nExemple de sentiment déjà calculé par Alpha Vantage :")
print(df[["entreprise_cible", "title", "overall_sentiment_score", "overall_sentiment_label"]].head(5))