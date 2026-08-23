import sys
from pathlib import Path
import psycopg2

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import POSTGRES_CONFIG

def creer_table():
    conn = psycopg2.connect(**POSTGRES_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS article_passages (
            id SERIAL PRIMARY KEY,
            article_id TEXT,
            title TEXT,
            entreprise_cible TEXT,
            chunk_text TEXT,
            chunk_index INTEGER,
            embedding VECTOR(768)
        )
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Table 'article_passages' créée avec succès.")

if __name__ == "__main__":
    creer_table()