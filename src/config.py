from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

# Racine du projet (calculée automatiquement, peu importe d'où le script est lancé)
ROOT_DIR = Path(__file__).resolve().parent.parent

# Dossiers de données
DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

SENTIMENTS_DIR = DATA_DIR / "sentiments"
JUSTIFICATIONS_DIR = DATA_DIR / "justifications"
EVALUATION_DIR = DATA_DIR / "evaluation"
REPORTS_DIR = DATA_DIR / "reports"
ENTITIES_DIR = DATA_DIR / "entities"
FIGURES_DIR = DATA_DIR / "figures"

# Fichiers bruts / préparés
ARTICLES_ALPHAVANTAGE = RAW_DIR / "articles_alphavantage.json"

# Résultats de sentiment
RESULTATS_FINBERT = SENTIMENTS_DIR / "sentiment_finbert.json"
RESULTATS_MISTRAL_RAG = SENTIMENTS_DIR / "sentiment_mistral_rag.json"

# Justifications et évaluation
FINBERT_JUSTIFICATIONS = JUSTIFICATIONS_DIR / "finbert_justifications.json"
EVALUATION_JUSTIFICATIONS = EVALUATION_DIR / "evaluation_justifications_finbert.json"
EVALUATION_JUSTIFICATIONS_RAG = EVALUATION_DIR / "evaluation_justifications_rag.json"
RESULTATS_MISTRAL = JUSTIFICATIONS_DIR / "mistral_justifications.json"

# Rapports de comparaison
COMPARAISON_3_METHODES = REPORTS_DIR / "comparaison_3_methodes.json"
COMPARAISON_RAG_API = REPORTS_DIR / "comparaison_mistral_rag_api.json"

# RAG
RAG_BANQUE = PROCESSED_DIR / "rag_banque.json"
RAG_TEST_SET = PROCESSED_DIR / "rag_test_set.json"

# Modèles utilisés
MODEL_MISTRAL = "mistral"
MODEL_QWEN_JUDGE = "qwen2.5:14b"
MODEL_EMBEDDINGS = "all-MiniLM-L6-v2"
MODEL_FINANCE_LLAMA = "martain7r/finance-llama-8b:q4_k_m"
MODEL_LLAMA3 = " llama3.1:8b"



POSTGRES_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
    "dbname": os.getenv("POSTGRES_DB", "finance_rag"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}
