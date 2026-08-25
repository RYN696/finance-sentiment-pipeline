import json
import sys
from pathlib import Path
import pandas as pd
from sklearn.metrics import (
    accuracy_score, confusion_matrix, classification_report,
    f1_score, cohen_kappa_score, matthews_corrcoef
)

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import PROCESSED_DIR, SENTIMENTS_DIR, JUSTIFICATIONS_DIR, REPORTS_DIR


def convertir_natif(label, score):
    if label:
        if label in ["Bullish", "Somewhat-Bullish"]:
            return "positive"
        if label in ["Bearish", "Somewhat-Bearish"]:
            return "negative"
        return "neutral"
    if score is not None:
        if score > 0.15:
            return "positive"
        if score < -0.15:
            return "negative"
        return "neutral"
    return None


def charger_natif():
    """Charge article_id -> sentiment natif converti, depuis articles_canonical.json"""
    with open(PROCESSED_DIR / "articles_canonical.json", "r", encoding="utf-8") as f:
        articles = json.load(f)

    natif_par_id = {}
    for a in articles:
        natif = convertir_natif(a.get("native_sentiment_label"), a.get("native_sentiment_score"))
        if natif:
            natif_par_id[a["article_id"]] = natif
    return natif_par_id


def comparer_methode(nom, chemin_fichier, label_key, natif_par_id):
    with open(chemin_fichier, "r", encoding="utf-8") as f:
        data = json.load(f)

    lignes = []
    for article in data:
        aid = article.get("article_id")
        natif = natif_par_id.get(aid)
        predit = article.get(label_key)
        # Normaliser "mixed" -> "neutral"
        if predit == "mixed":
            predit = "neutral"
        if natif and predit:
            lignes.append({"native": natif, "predicted": predit})

    df = pd.DataFrame(lignes)

    if len(df) == 0:
        print(f"\n{nom} : aucun article avec référence native, ignoré.")
        return None

    y_true = df["native"]
    y_pred = df["predicted"]

    accuracy = accuracy_score(y_true, y_pred)
    macro_f1 = f1_score(y_true, y_pred, average="macro", zero_division=0)
    kappa = cohen_kappa_score(y_true, y_pred)
    mcc = matthews_corrcoef(y_true, y_pred)

    print(f"\n=== {nom} (n={len(df)}) ===")
    print(f"Accuracy      : {accuracy:.3f}")
    print(f"Macro-F1      : {macro_f1:.3f}")
    print(f"Cohen's Kappa : {kappa:.3f}")
    print(f"MCC           : {mcc:.3f}")

    labels = sorted(set(y_true) | set(y_pred))
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    print("\nMatrice de confusion (lignes=natif, colonnes=prédit) :")
    print(pd.DataFrame(cm, index=labels, columns=labels))

    print("\nRapport par classe :")
    print(classification_report(y_true, y_pred, zero_division=0))

    return {
        "methode": nom,
        "n_articles": len(df),
        "accuracy": round(accuracy, 3),
        "macro_f1": round(macro_f1, 3),
        "cohen_kappa": round(kappa, 3),
        "mcc": round(mcc, 3)
    }


def run():
    natif_par_id = charger_natif()
    print(f"Articles avec référence native disponible : {len(natif_par_id)}")

    configs = [
        {"nom": "FinBERT", "chemin": SENTIMENTS_DIR / "sentiment_finbert.json", "label_key": "finbert_label"},
        {"nom": "Mistral", "chemin": JUSTIFICATIONS_DIR / "mistral_justifications.json", "label_key": "mistral_label"},
        {"nom": "Finance-Llama", "chemin": SENTIMENTS_DIR / "sentiment_financellama.json", "label_key": "financellama_label"},
    ]

    resultats = []
    for cfg in configs:
        if not cfg["chemin"].exists():
            print(f"Fichier introuvable, ignoré : {cfg['chemin']}")
            continue
        res = comparer_methode(cfg["nom"], cfg["chemin"], cfg["label_key"], natif_par_id)
        if res:
            resultats.append(res)

    tableau = pd.DataFrame(resultats)
    print("\n\n=== TABLEAU RÉCAPITULATIF ===")
    print(tableau)

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = REPORTS_DIR / "benchmark_sentiments.json"
    tableau.to_json(output_path, orient="records", indent=2)
    print(f"\nSauvegardé dans {output_path}")

    return tableau


if __name__ == "__main__":
    run()