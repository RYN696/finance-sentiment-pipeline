import pandas as pd

def convertir_alphavantage(label):
    if label in ["Bullish", "Somewhat-Bullish"]:
        return "positive"
    elif label in ["Bearish", "Somewhat-Bearish"]:
        return "negative"
    return "neutral"

def comparer_deux_methodes(df, colonne_a, colonne_b, nom_a="Méthode A", nom_b="Méthode B"):
    """Calcule le taux d'accord et la matrice de confusion entre deux colonnes de labels."""
    taux_accord = (df[colonne_a] == df[colonne_b]).mean() * 100

    print(f"Nombre d'articles comparés : {len(df)}")
    print(f"Taux d'accord {nom_a} / {nom_b} : {taux_accord:.1f}%")
    print(f"\nMatrice de confusion {nom_a} (lignes) vs {nom_b} (colonnes) :")
    print(pd.crosstab(df[colonne_a], df[colonne_b]))

    return taux_accord

def normaliser_mistral(df, colonne="mistral_label"):
    df[colonne + "_normalise"] = df[colonne].replace("mixed", "neutral")
    return df