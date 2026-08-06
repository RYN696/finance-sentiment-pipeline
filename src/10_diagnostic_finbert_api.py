import json
import pandas as pd

with open("data/results/comparaison_3_methodes.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Matrice de confusion FinBERT vs API
print("Matrice de confusion FinBERT (lignes) vs API (colonnes) :")
print(pd.crosstab(df["finbert_label"], df["api_label_normalise"]))