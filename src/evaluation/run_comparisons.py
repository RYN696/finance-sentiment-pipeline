import sys
from pathlib import Path
import json
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import RESULTATS_FINBERT, RESULTATS_MISTRAL, RESULTATS_MISTRAL_RAG
from evaluation.compare import comparer_deux_methodes, convertir_alphavantage, normaliser_mistral

def comparer_finbert_api():
    with open(RESULTATS_FINBERT, "r", encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df["api_label_normalise"] = df["alphavantage_label"].apply(convertir_alphavantage)
    return comparer_deux_methodes(df, "finbert_label", "api_label_normalise", "FinBERT", "API")

def comparer_mistral_api():
    with open(RESULTATS_MISTRAL, "r", encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df = normaliser_mistral(df)
    df["api_label_normalise"] = df["alphavantage_label"].apply(convertir_alphavantage)
    return comparer_deux_methodes(df, "mistral_label_normalise", "api_label_normalise", "Mistral", "API")

def comparer_rag_api():
    with open(RESULTATS_MISTRAL_RAG, "r", encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df = normaliser_mistral(df)
    return comparer_deux_methodes(df, "mistral_label_normalise", "api_label_normalise", "Mistral+RAG", "API")

if __name__ == "__main__":
    print("=== FinBERT vs API ===")
    comparer_finbert_api()
    print("\n=== Mistral vs API ===")
    comparer_mistral_api()
    print("\n=== Mistral+RAG vs API ===")
    comparer_rag_api()