import json
import pandas as pd

# Charger les articles collectés
with open("data/articles.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

# Convertir en tableau pandas
df = pd.DataFrame(articles)

print("Nombre total d'articles :", len(df))
print("\nColonnes disponibles :", list(df.columns))
print("\nRépartition par entreprise :")
print(df["entreprise_cible"].value_counts())

print("\nAperçu des 3 premiers titres :")
print(df[["entreprise_cible", "title"]].head(3))

# Vérifier s'il y a des doublons (même titre exact)
doublons = df.duplicated(subset=["title"]).sum()
print(f"\nNombre de doublons détectés : {doublons}")

# Filtrage : garder seulement les articles où l'entreprise est explicitement citée
def est_pertinent(row):
    texte = f"{row['title']} {row['description']}".lower()
    return row["entreprise_cible"].lower() in texte

df_filtre = df[df.apply(est_pertinent, axis=1)]

print(f"\nAvant filtrage : {len(df)} articles")
print(f"Après filtrage : {len(df_filtre)} articles")
print(f"Articles supprimés : {len(df) - len(df_filtre)}")

print("\nTitres après filtrage :")
print(df_filtre[["entreprise_cible", "title"]])

print("\n--- Articles Sanofi supprimés (pour comprendre pourquoi) ---")
sanofi_supprimes = df[(df["entreprise_cible"] == "Sanofi") & (~df.index.isin(df_filtre.index))]
for _, row in sanofi_supprimes.iterrows():
    print("\nTitre :", row["title"])
    print("Description :", row["description"])