import json
import random
import sys
from pathlib import Path
from sentence_transformers import SentenceTransformer

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import ARTICLES_PREPARES, RAG_BANQUE, RAG_TEST_SET, PROCESSED_DIR, MODEL_EMBEDDINGS

random.seed(42)

def convertir_alphavantage(label):
    if label in ["Bullish", "Somewhat-Bullish"]:
        return "positive"
    elif label in ["Bearish", "Somewhat-Bearish"]:
        return "negative"
    return "neutral"

def construire_banque(taille_banque=150):
    with open(ARTICLES_PREPARES, "r", encoding="utf-8") as f:
        articles = json.load(f)

    for a in articles:
        a["api_label_normalise"] = convertir_alphavantage(a.get("overall_sentiment_label", "Neutral"))

    random.shuffle(articles)
    banque = articles[:taille_banque]
    test_set = articles[taille_banque:]

    print(f"Banque : {len(banque)} articles | Test set : {len(test_set)} articles")

    print("Chargement du modèle d'embeddings...")
    model = SentenceTransformer(MODEL_EMBEDDINGS)

    textes_banque = [f"{a['title']} {a['summary']}" for a in banque]
    embeddings = model.encode(textes_banque, show_progress_bar=True)

    for i, a in enumerate(banque):
        a["embedding"] = embeddings[i].tolist()

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    with open(RAG_BANQUE, "w", encoding="utf-8") as f:
        json.dump(banque, f, ensure_ascii=False)
    with open(RAG_TEST_SET, "w", encoding="utf-8") as f:
        json.dump(test_set, f, ensure_ascii=False, indent=2)

    print(f"Sauvegardé : {RAG_BANQUE} et {RAG_TEST_SET}")
    return banque, test_set

if __name__ == "__main__":
    construire_banque()