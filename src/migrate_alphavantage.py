import json
import sqlite3
from database import DB_PATH, init_db

def get_ticker_sentiment(article):
    """Extrait le sentiment spécifique à l'entreprise ciblée depuis ticker_sentiment"""
    ticker_data = article.get("ticker_sentiment", [])
    for item in ticker_data:
        # On prend le premier ticker (celui qui correspond à notre recherche)
        try:
            score = float(item.get("ticker_sentiment_score", 0))
            label = item.get("ticker_sentiment_label", "")
            return score, label
        except (ValueError, TypeError):
            continue
    return None, None

def migrate():
    init_db()

    with open("data/articles_alphavantage.json", "r", encoding="utf-8") as f:
        articles = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    inseres = 0
    ignores = 0

    for article in articles:
        ticker_score, ticker_label = get_ticker_sentiment(article)
        topics_str = json.dumps(article.get("topics", []), ensure_ascii=False)

        try:
            cursor.execute("""
                INSERT INTO articles (
                    entreprise_cible, title, summary, source, url, time_published,
                    overall_sentiment_score, overall_sentiment_label,
                    ticker_sentiment_score, ticker_sentiment_label, topics
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                article["entreprise_cible"],
                article["title"],
                article.get("summary", ""),
                article.get("source", ""),
                article["url"],
                article.get("time_published", ""),
                article.get("overall_sentiment_score"),
                article.get("overall_sentiment_label"),
                ticker_score,
                ticker_label,
                topics_str
            ))
            inseres += 1
        except sqlite3.IntegrityError:
            ignores += 1  # doublon (même url déjà présente)

    conn.commit()
    conn.close()

    print(f"Articles insérés : {inseres}")
    print(f"Articles ignorés (doublons) : {ignores}")

if __name__ == "__main__":
    migrate()