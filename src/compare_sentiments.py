import json
import pandas as pd

with open("data/resultats_finbert.json", "r", encoding="utf-8") as f:
    finbert = json.load(f)

with open("data/resultats_mistral_propres.json", "r", encoding="utf-8") as f:
    mistral = json.load(f)

df_finbert = pd.DataFrame(finbert)[["title", "entreprise_cible", "finbert_label"]]
df_mistral = pd.DataFrame(mistral)[["title", "mistral_label", "mistral_justification"]]

# Fusionner sur le titre (identifiant commun entre les deux fichiers)
df = pd.merge(df_finbert, df_mistral, on="title", how="inner")

print(f"Nombre d'articles comparés : {len(df)}")

# Uniformiser "mixed" vers "neutral" pour une comparaison équitable
df["mistral_label_normalise"] = df["mistral_label"].replace("mixed", "neutral")

# Calcul de l'accord entre les deux méthodes
df["accord"] = df["finbert_label"] == df["mistral_label_normalise"]
taux_accord = df["accord"].mean() * 100

print(f"\nTaux d'accord FinBERT / Mistral : {taux_accord:.1f}%")

print("\nRépartition FinBERT :")
print(df["finbert_label"].value_counts())

print("\nRépartition Mistral :")
print(df["mistral_label_normalise"].value_counts())

# Voir les cas de désaccord
desaccords = df[~df["accord"]]
print(f"\nNombre de désaccords : {len(desaccords)}")
print("\nExemples de désaccords :")
print(desaccords[["entreprise_cible", "title", "finbert_label", "mistral_label_normalise"]].head(10))

df.to_json("data/comparaison_finbert_mistral.json", orient="records", force_ascii=False, indent=2)
print("\nSauvegardé dans data/comparaison_finbert_mistral.json")