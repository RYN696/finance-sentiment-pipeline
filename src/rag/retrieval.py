import sys
from pathlib import Path
import psycopg2
from sentence_transformers import SentenceTransformer

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import POSTGRES_CONFIG, MODEL_EMBEDDINGS

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_EMBEDDINGS)
    return _model

def rechercher_passages_similaires(texte_article, entreprise_cible=None, k=5):
    model = get_model()
    embedding = model.encode([texte_article])[0].tolist()

    conn = psycopg2.connect(**POSTGRES_CONFIG)
    cur = conn.cursor()

    cur.execute(
         """SELECT article_id, title, chunk_text, embedding <=> %s::vector AS distance
            FROM article_passages
            WHERE entreprise_cible = %s
            ORDER BY distance ASC
            LIMIT %s""",
         (embedding, entreprise_cible, k)
    )

    resultats = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {"article_id": r[0], "title": r[1], "chunk_text": r[2], "distance": r[3]}
        for r in resultats
    ]

if __name__ == "__main__":
    resultats = rechercher_passages_similaires("Apple reported record quarterly revenue", entreprise_cible="Apple")
    for r in resultats:
        print(f"[{r['distance']:.3f}] {r['title']} -> {r['chunk_text'][:100]}")