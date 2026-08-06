import json
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import ARTICLES_ALPHAVANTAGE, ARTICLES_PREPARES, PROCESSED_DIR

def preparer():
    with open(ARTICLES_ALPHAVANTAGE, "r", encoding="utf-8") as f:
        articles = json.load(f)

    df = pd.DataFrame(articles)
    print(f"Nombre total d'articles : {len(df)}")

    df["texte_complet"] = df["title"].fillna("") + " " + df["summary"].fillna("")
    df["longueur_texte"] = df["texte_complet"].str.len()

    doublons = df.duplicated(subset=["title"]).sum()
    print(f"Doublons détectés : {doublons}")

    df_propre = df.drop_duplicates(subset=["title"]).reset_index(drop=True)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df_propre.to_json(ARTICLES_PREPARES, orient="records", force_ascii=False, indent=2)

    print(f"{len(df_propre)} articles sauvegardés dans {ARTICLES_PREPARES}")
    return df_propre

if __name__ == "__main__":
    preparer()