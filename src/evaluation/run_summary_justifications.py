import sys
from pathlib import Path
import json
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import EVALUATION_DIR

CRITERES = ["faithfulness", "relevance", "completeness", "clarity", "hallucination", "consistency", "evidence_grounding"]

def charger_evaluation(nom_fichier):
    with open(EVALUATION_DIR / nom_fichier, "r", encoding="utf-8") as f:
        return pd.DataFrame(json.load(f))

def resumer(df, nom_methode):
    scores_moyens = df[CRITERES].mean().round(2)
    score_global = round(scores_moyens.mean(), 2)
    return scores_moyens, score_global

def run():
    df_finbert = charger_evaluation("evaluation_justifications_finbert.json")
    df_rag = charger_evaluation("evaluation_justifications_rag.json")

    scores_finbert, global_finbert = resumer(df_finbert, "FinBERT")
    scores_rag, global_rag = resumer(df_rag, "Mistral+RAG")

    print("=== Comparaison de la qualité des justifications ===\n")

    tableau = pd.DataFrame({
        "FinBERT (justifié par Mistral)": scores_finbert,
        "Mistral+RAG (justification native)": scores_rag
    })
    print(tableau)

    print(f"\nScore global moyen FinBERT : {global_finbert}/5")
    print(f"Score global moyen Mistral+RAG : {global_rag}/5")

    # Sauvegarder le résumé
    tableau.to_json(EVALUATION_DIR / "resume_comparaison_justifications.json", orient="index", indent=2)
    print(f"\nSauvegardé dans {EVALUATION_DIR / 'resume_comparaison_justifications.json'}")

    return tableau

if __name__ == "__main__":
    run()