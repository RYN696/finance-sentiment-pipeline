import json
import sys
from pathlib import Path
import psycopg2
from sentence_transformers import SentenceTransformer

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import PROCESSED_DIR, POSTGRES_CONFIG, MODEL_EMBEDDINGS

def decouper_en_chunks(texte, phrases_par_chunk=2):

    phrases = [p.strip() for p in texte.split(".") if len(p.strip()) > 10]
    chunks = []
    for i in range(0, len(phrases), phrases_par_chunk):
        chunk = ". ".join(phrases[i:i + phrases_par_chunk]) + "."
        chunks.append(chunk)
    return chunks

def peupler():
    with open(PROCESSED_DIR / "articles_canonical.json", "r", encoding="utf-8") as f:
        articles = json.load(f)

    print(f"Chargement du modèle d'embeddings...")
    model = SentenceTransformer(MODEL_EMBEDDINGS)

    conn = psycopg2.connect(**POSTGRES_CONFIG)
    cur = conn.cursor()

    # Vider la table avant de repeupler
    cur.execute("TRUNCATE TABLE article_passages RESTART IDENTITY")

    total_chunks = 0
    for i, article in enumerate(articles):
        texte_complet = f"{article['title']}. {article['text']}"
        chunks = decouper_en_chunks(texte_complet)

        if not chunks:
            continue

        embeddings = model.encode(chunks, show_progress_bar=False)

        for idx, (chunk, emb) in enumerate(zip(chunks, embeddings)):
            cur.execute(
                """INSERT INTO article_passages (article_id, title, entreprise_cible, chunk_text, chunk_index, embedding)
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (article["article_id"], article["title"], article["entreprise_cible"], chunk, idx, emb.tolist())
            )
            total_chunks += 1

        if (i + 1) % 20 == 0:
            print(f"  {i + 1}/{len(articles)} articles traités, {total_chunks} chunks insérés...")
            conn.commit()

    conn.commit()
    cur.close()
    conn.close()

    print(f"\nTerminé ! {total_chunks} chunks insérés depuis {len(articles)} articles.")

if __name__ == "__main__":
    peupler()