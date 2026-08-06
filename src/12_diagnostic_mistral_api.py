import json
import pandas as pd

with open("data/results/resultats_mistral_v2.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Normaliser Mistral (au cas où "mixed" apparaît)
df["mistral_label_normalise"] = df["mistral_label"].replace("mixed", "neutral")

# Convertir le label Alpha Vantage (5 niveaux) vers 3 niveaux
def convertir_alphavantage(label):
    if label in ["Bullish", "Somewhat-Bullish"]:
        return "positive"
    elif label in ["Bearish", "Somewhat-Bearish"]:
        return "negative"
    else:
        return "neutral"

df["api_label_normalise"] = df["alphavantage_label"].apply(convertir_alphavantage)

taux_accord = (df["mistral_label_normalise"] == df["api_label_normalise"]).mean() * 100
print(f"Nombre d'articles comparés : {len(df)}")
print(f"Taux d'accord Mistral v2 / API : {taux_accord:.1f}%")

print("\nMatrice de confusion Mistral v2 (lignes) vs API (colonnes) :")
print(pd.crosstab(df["mistral_label_normalise"], df["api_label_normalise"]))

print("\nRépartition Mistral v2 :")
print(df["mistral_label_normalise"].value_counts())

print("\nRépartition API :")
print(df["api_label_normalise"].value_counts())

df.to_json("data/results/comparaison_mistral_v2_api.json", orient="records", force_ascii=False, indent=2)
print("\nSauvegardé dans data/results/comparaison_mistral_v2_api.json")