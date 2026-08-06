import json
import pandas as pd

with open("data/results/resultats_mistral_rag.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Normaliser Mistral (au cas où "mixed" apparaît)
df["mistral_label_normalise"] = df["mistral_label"].replace("mixed", "neutral")

taux_accord = (df["mistral_label_normalise"] == df["api_label_normalise"]).mean() * 100

print(f"Nombre d'articles testés (RAG) : {len(df)}")
print(f"Taux d'accord Mistral + RAG / API : {taux_accord:.1f}%")

print("\nMatrice de confusion Mistral+RAG (lignes) vs API (colonnes) :")
print(pd.crosstab(df["mistral_label_normalise"], df["api_label_normalise"]))

print("\nRépartition Mistral+RAG :")
print(df["mistral_label_normalise"].value_counts())

print("\nRépartition API :")
print(df["api_label_normalise"].value_counts())

df.to_json("data/results/comparaison_mistral_rag_api.json", orient="records", force_ascii=False, indent=2)
print("\nSauvegardé dans data/results/comparaison_mistral_rag_api.json")