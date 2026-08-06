import json
import pandas as pd

with open("data/results/resultats_finbert.json", "r", encoding="utf-8") as f:
    finbert = json.load(f)

with open("data/results/resultats_mistral.json", "r", encoding="utf-8") as f:
    mistral = json.load(f)

df_finbert = pd.DataFrame(finbert)[["title", "entreprise_cible", "finbert_label", "alphavantage_label"]]
df_mistral = pd.DataFrame(mistral)[["title", "mistral_label", "mistral_justification"]]

df = pd.merge(df_finbert, df_mistral, on="title", how="inner")

df["mistral_label_normalise"] = df["mistral_label"].replace("mixed", "neutral")

# Convertir Alpha Vantage (5 niveaux) vers 3 niveaux
def convertir_alphavantage(label):
    if label in ["Bullish", "Somewhat-Bullish"]:
        return "positive"
    elif label in ["Bearish", "Somewhat-Bearish"]:
        return "negative"
    else:
        return "neutral"

df["api_label_normalise"] = df["alphavantage_label"].apply(convertir_alphavantage)

# Calcul des 3 taux d'accord (paires)
accord_finbert_mistral = (df["finbert_label"] == df["mistral_label_normalise"]).mean() * 100
accord_finbert_api = (df["finbert_label"] == df["api_label_normalise"]).mean() * 100
accord_mistral_api = (df["mistral_label_normalise"] == df["api_label_normalise"]).mean() * 100

print(f"Nombre d'articles comparés : {len(df)}\n")
print(f"Taux d'accord FinBERT / Mistral : {accord_finbert_mistral:.1f}%")
print(f"Taux d'accord FinBERT / API (Alpha Vantage) : {accord_finbert_api:.1f}%")
print(f"Taux d'accord Mistral / API (Alpha Vantage) : {accord_mistral_api:.1f}%")

print("\nRépartition FinBERT :")
print(df["finbert_label"].value_counts())
print("\nRépartition Mistral :")
print(df["mistral_label_normalise"].value_counts())
print("\nRépartition API (Alpha Vantage) :")
print(df["api_label_normalise"].value_counts())

# Cas où les 3 méthodes sont d'accord
df["accord_total"] = (
    (df["finbert_label"] == df["mistral_label_normalise"]) &
    (df["mistral_label_normalise"] == df["api_label_normalise"])
)
taux_accord_total = df["accord_total"].mean() * 100
print(f"\nTaux d'accord entre les 3 méthodes en même temps : {taux_accord_total:.1f}%")

df.to_json("data/results/comparaison_3_methodes.json", orient="records", force_ascii=False, indent=2)
print("\nSauvegardé dans data/results/comparaison_3_methodes.json")