import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from data_collection.collect_alphavantage import collecter
from sentiment.run_finbert import run as run_finbert
from sentiment.run_mistral import run as run_mistral
from rag.build_bank import construire_banque
from rag.run_mistral_rag import run as run_rag
from evaluation.justify_finbert import run as justifier
from evaluation.evaluate_justifications import run as evaluer
from evaluation.run_evaluate_rag import run_evaluation_rag
from evaluation.run_evaluate_marketaux import run_evaluation_marketaux

ETAPES = {
    "collect": collecter,
    "finbert": run_finbert,
    "mistral": run_mistral,
    "rag_bank": construire_banque,
    "rag_sentiment": run_rag,
    "justify": justifier,
    "evaluate": evaluer,
    "evaluate_rag": run_evaluation_rag,
    "evaluate_marketaux": run_evaluation_marketaux,
}

def run_pipeline(etapes_a_executer):
    for nom in etapes_a_executer:
        if nom not in ETAPES:
            print(f"Étape inconnue : {nom}")
            continue
        print(f"\n{'='*50}\nÉTAPE : {nom}\n{'='*50}")
        ETAPES[nom]()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline d'analyse de sentiment financier")
    parser.add_argument(
        "--steps",
        nargs="+",
        default=list(ETAPES.keys()),
        help=f"Étapes à exécuter parmi : {list(ETAPES.keys())}"
    )
    args = parser.parse_args()
    run_pipeline(args.steps)