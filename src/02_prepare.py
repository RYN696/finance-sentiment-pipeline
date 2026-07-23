import json
import pandas as pd

with open("data/raw/articles_alphavantage.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

df = pd.DataFrame(articles)

print(f"Nombre total d'articles : {len(df)}")

# Vérifier les champs vides
print("\nValeurs manquantes par colonne :")
print(df[["title", "summary", "overall_sentiment_score"]].isnull().sum())

# Vérifier les titres/summary vides (chaîne vide, pas juste NaN)
titres_vides = (df["title"].fillna("").str.strip() == "").sum()
summary_vides = (df["summary"].fillna("").str.strip() == "").sum()
print(f"\nTitres vides : {titres_vides}")
print(f"Summary vides : {summary_vides}")

# Longueur du texte (titre + summary combinés)
df["texte_complet"] = df["title"].fillna("") + " " + df["summary"].fillna("")
df["longueur_texte"] = df["texte_complet"].str.len()

print(f"\nLongueur moyenne du texte : {df['longueur_texte'].mean():.0f} caractères")
print(f"Longueur minimale : {df['longueur_texte'].min()}")
print(f"Longueur maximale : {df['longueur_texte'].max()}")

# Combien d'articles ont un texte très court (potentiellement inutilisable)
tres_courts = (df["longueur_texte"] < 30).sum()
print(f"\nArticles avec texte très court (<30 caractères) : {tres_courts}")

# Doublons
doublons = df.duplicated(subset=["title"]).sum()
print(f"Doublons détectés : {doublons}")

# Sauvegarder une version propre et unique, prête pour FinBERT/FinGPT
df_propre = df.drop_duplicates(subset=["title"]).reset_index(drop=True)
df_propre.to_json("data/processed/articles_prepares.json", orient="records", force_ascii=False, indent=2)
print(f"\n{len(df_propre)} articles sauvegardés dans data/processed/articles_prepares.json")