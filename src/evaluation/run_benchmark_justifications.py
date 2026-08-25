import json
import sys
from pathlib import Path
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import EVALUATION_DIR, REPORTS_DIR

CRITERES = ["faithfulness", "relevance", "completeness", "clarity", "hallucination", "consistency", "evidencegrounding"]

FICHIERS = {
    "Llama3.1": "evaluation_finbert.json",
    "Mistral": "evaluation_mistral.json",
    "Finance-Llama": "evaluation_financellama.json",
    "Llama3.1-RAG": "evaluation_llama_rag.json",
    "Mistral-RAG": "evaluation_mistral_rag.json",
    "Finance-Llama-RAG": "evaluation_financellama_rag.json"
}

def charger(nom_fichier):
    with open(EVALUATION_DIR / nom_fichier, "r", encoding="utf-8") as f:
        df = pd.DataFrame(json.load(f))
    df.columns = [c.replace("evidence_grounding", "evidencegrounding") for c in df.columns]
    return df

def run():
    tableau = {}

    for methode, fichier in FICHIERS.items():
        chemin = EVALUATION_DIR / fichier
        if not chemin.exists():
            print(f"Fichier manquant, ignoré : {fichier}")
            continue

        df = charger(fichier)
        criteres_presents = [c for c in CRITERES if c in df.columns]
        scores_moyens = df[criteres_presents].mean().round(2)
        tableau[methode] = scores_moyens

    resultat = pd.DataFrame(tableau)
    resultat.loc["SCORE GLOBAL"] = resultat.mean().round(2)

    print("=== Benchmark qualité des justifications ===\n")
    print(resultat)

    EVALUATION_DIR.mkdir(parents=True, exist_ok=True)
    output_path = REPORTS_DIR / "benchmark_justifications.json"
    resultat.to_json(output_path, orient="index", indent=2)
    print(f"\nSauvegardé dans {output_path}")

    return resultat

if __name__ == "__main__":
    run()