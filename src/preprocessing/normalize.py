import json
import hashlib
import sys
from pathlib import Path
from collections import Counter

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import RAW_DIR, PROCESSED_DIR

def generer_id(url, title, source_name):
    base = url if url else f"{source_name}_{title}"
    return hashlib.md5(base.encode("utf-8")).hexdigest()

def normaliser_alphavantage(article):
    return {
        "article_id": generer_id(article.get("url"), article["title"], "alphavantage"),
        "title": article["title"],
        "text": article.get("summary", ""),
        "source_name": "alphavantage",
        "entreprise_cible": article["entreprise_cible"],
        "published_at": article.get("time_published", ""),
        "url": article.get("url"),
        "native_sentiment_score": article.get("overall_sentiment_score"),
        "native_sentiment_label": article.get("overall_sentiment_label"),
        "metadata": {
            "topics": article.get("topics", []),
        }
    }

def normaliser_marketaux(article):
    return {
        "article_id": generer_id(article.get("url"), article["title"], "marketaux"),
        "title": article["title"],
        "text": article.get("summary", ""),
        "source_name": "marketaux",
        "entreprise_cible": article["entreprise_cible"],
        "published_at": article.get("published_at", ""),
        "url": article.get("url"),
        "native_sentiment_score": article.get("marketaux_sentiment"),
        "native_sentiment_label": None,
        "metadata": {
            "match_score": article.get("match_score"),
        }
    }

def normaliser_secedgar(article):
    texte = article.get("texte", "")
    return {
        "article_id": generer_id(None, texte[:100], "secedgar"),
        "title": article.get("title", texte[:80]),
        "text": texte,
        "source_name": "secedgar",
        "entreprise_cible": article["entreprise_cible"],
        "published_at": article.get("filing_date", ""),
        "url": None,
        "native_sentiment_score": None,
        "native_sentiment_label": None,
        "metadata": {
            "form_type": article.get("form_type"),
        }
    }

def normaliser():
    tous_les_articles = []

    with open(RAW_DIR / "articles_alphavantage.json", "r", encoding="utf-8") as f:
        for a in json.load(f):
            tous_les_articles.append(normaliser_alphavantage(a))

    with open(RAW_DIR / "articles_marketaux.json", "r", encoding="utf-8") as f:
        for a in json.load(f):
            tous_les_articles.append(normaliser_marketaux(a))

    secedgar_path = RAW_DIR / "secedgar_8k.json"
    if secedgar_path.exists():
        with open(secedgar_path, "r", encoding="utf-8") as f:
            for a in json.load(f):
                tous_les_articles.append(normaliser_secedgar(a))

    vus = set()
    articles_uniques = []
    for a in tous_les_articles:
        if a["article_id"] not in vus:
            vus.add(a["article_id"])
            articles_uniques.append(a)

    print(f"Total avant dédup inter-source : {len(tous_les_articles)}")
    print(f"Total après dédup : {len(articles_uniques)}")
    print("\nRépartition par source :")
    print(Counter(a["source_name"] for a in articles_uniques))

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    output_path = PROCESSED_DIR / "articles_canonical.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(articles_uniques, f, ensure_ascii=False, indent=2)

    print(f"\nSauvegardé dans {output_path}")
    return articles_uniques

if __name__ == "__main__":
    normaliser()