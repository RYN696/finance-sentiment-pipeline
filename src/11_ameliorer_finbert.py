import json
import pandas as pd

# Charger les scores bruts de FinBERT (avec les probabilités)
with open("data/results/resultats_finbert.json", "r", encoding="utf-8") as f:
    finbert = json.load(f)

df_finbert = pd.DataFrame(finbert)

# Charger la comparaison existante (contient déjà le label API normalisé)
with open("data/results/comparaison_3_methodes.json", "r", encoding="utf-8") as f:
    comparaison = json.load(f)

df_comp = pd.DataFrame(comparaison)[["title", "api_label_normalise"]]

# Fusionner pour avoir probabilités FinBERT + label API au même endroit
df = pd.merge(df_finbert, df_comp, on="title", how="inner")

def reclassifier_avec_seuil(row, marge_minimale=0.15):
    scores = {
        "positive": row["finbert_positive"],
        "negative": row["finbert_negative"],
        "neutral": row["finbert_neutral"]
    }
    trie = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    meilleur_label, meilleur_score = trie[0]
    deuxieme_label, deuxieme_score = trie[1]

    # Si l'écart entre le 1er et le 2e choix est faible, on classe en neutral
    if (meilleur_score - deuxieme_score) < marge_minimale and meilleur_label != "neutral":
        return "neutral"
    return meilleur_label

df["finbert_label_ajuste"] = df.apply(reclassifier_avec_seuil, axis=1)

# Comparer l'ancien taux d'accord vs le nouveau
accord_avant = (df["finbert_label"] == df["api_label_normalise"]).mean() * 100
accord_apres = (df["finbert_label_ajuste"] == df["api_label_normalise"]).mean() * 100

print(f"Taux d'accord FinBERT (original) / API : {accord_avant:.1f}%")
print(f"Taux d'accord FinBERT (ajusté avec seuil) / API : {accord_apres:.1f}%")

print("\nNouvelle répartition FinBERT ajusté :")
print(df["finbert_label_ajuste"].value_counts())

print("\nNouvelle matrice de confusion (ajusté) :")
print(pd.crosstab(df["finbert_label_ajuste"], df["api_label_normalise"]))

df.to_json("data/results/finbert_ajuste.json", orient="records", force_ascii=False, indent=2)
print("\nSauvegardé dans data/results/finbert_ajuste.json")