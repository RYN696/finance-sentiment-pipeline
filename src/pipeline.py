import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from data_collection.collect_alphavantage import collecter as collect_alphavantage
from data_collection.collect_marketaux import collecter as collect_marketaux
from data_collection.collect_secedgar import collecter as collect_secedgar
from preprocessing.normalize import normaliser as normalize
from extraction.extract_entities import run as extract_entities
from sentiment.run_finbert import run as run_finbert
from sentiment.run_mistral import run as run_mistral
from sentiment.justify_finbert import run as justify_finbert
from sentiment.run_financellama import run as run_financellama
from rag.build_bank import construire_banque as build_rag_bank
from rag.run_mistral_rag import run as run_mistral_rag
from evaluation.run_evaluate_all import run_all as evaluate_all
from evaluation.run_benchmark_justifications import run as benchmark_justifications

ETAPES = {
    "collect_alphavantage": collect_alphavantage,
    "collect_marketaux": collect_marketaux,
    "collect_secedgar": collect_secedgar,
    "normalize": normalize,
    "extract_entities": extract_entities,
    "finbert": run_finbert,
    "mistral": run_mistral,
    "justify_finbert": justify_finbert,
    "financellama": run_financellama,
    "rag_bank": build_rag_bank,
    "rag_sentiment": run_mistral_rag,
    "evaluate_all": evaluate_all,
    "benchmark_justifications": benchmark_justifications,
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
        help=f"Étapes disponibles : {list(ETAPES.keys())}"
    )
    args = parser.parse_args()
    run_pipeline(args.steps)