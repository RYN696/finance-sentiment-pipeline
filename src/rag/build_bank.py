import json
import random
import sys
from pathlib import Path
from sentence_transformers import SentenceTransformer

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import PROCESSED_DIR, RAG_BANQUE, RAG_TEST_SET, MODEL_EMBEDDINGS

random.seed(42)

def convertir_sentiment(article):
    """Utilise le sentiment natif si disponible, sinon retourne None (article non utilisable pour la banque)."""
    label = article.get("native_sentiment_label")
    score = article.get("native_sentiment_score")

    if label:
        if label in ["Bullish", "Somewhat-Bullish"]:
            return "positive"
        elif label in ["Bearish", "Somewhat-Bearish"]:
            return "negative"
        return "neutral"

    if score is not None:
        if score > 0.15:
            return "positive"
        elif score < -0.15:
            return "negative"
        return "neutral"

    return None

def construire_banque(taille_banque=50):
    with open(PROCESSED_DIR / "articles_canonical.json", "r", encoding="utf-8") as f:
        articles = json.load(f)

    # Ne garder que les articles ayant un sentiment de référence (nécessaire pour la banque)
    for a in articles:
        a["ref_sentiment"] = convertir_sentiment(a)

    articles_avec_ref = [a for a in articles if a["ref_sentiment"] is not None]
    articles_sans_ref = [a for a in articles if a["ref_sentiment"] is None]

    print(f"Articles avec référence native : {len(articles_avec_ref)}")
    print(f"Articles sans référence (iront dans le test set) : {len(articles_sans_ref)}")

    random.shuffle(articles_avec_ref)
    taille_banque = min(taille_banque, len(articles_avec_ref) // 2)
    banque = articles_avec_ref[:taille_banque]
    test_set = articles_avec_ref[taille_banque:] + articles_sans_ref

    print(f"Banque : {len(banque)} articles | Test set : {len(test_set)} articles")

    print("Chargement du modèle d'embeddings...")
    model = SentenceTransformer(MODEL_EMBEDDINGS)

    textes_banque = [f"{a['title']} {a['text']}" for a in banque]
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