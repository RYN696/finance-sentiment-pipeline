from pathlib import Path

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
ARTICLES_PREPARES = PROCESSED_DIR / "articles_prepares.json"

# Résultats de sentiment
RESULTATS_FINBERT = SENTIMENTS_DIR / "sentiment_finbert.json"
RESULTATS_MISTRAL = SENTIMENTS_DIR / "sentiment_mistral.json"
RESULTATS_MISTRAL_RAG = SENTIMENTS_DIR / "sentiment_mistral_rag.json"

# Justifications et évaluation
FINBERT_JUSTIFICATIONS = JUSTIFICATIONS_DIR / "finbert_justifications.json"
EVALUATION_JUSTIFICATIONS = EVALUATION_DIR / "evaluation_justifications.json"

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