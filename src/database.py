import sqlite3
import os

DB_PATH = "data/articles.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entreprise_cible TEXT,
            title TEXT,
            summary TEXT,
            source TEXT,
            url TEXT UNIQUE,
            time_published TEXT,
            overall_sentiment_score REAL,
            overall_sentiment_label TEXT,
            ticker_sentiment_score REAL,
            ticker_sentiment_label TEXT,
            topics TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("Base de données initialisée :", DB_PATH)

if __name__ == "__main__":
    init_db()