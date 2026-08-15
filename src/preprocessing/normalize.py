import json
import hashlib
import sys
from pathlib import Path
from collections import Counter, defaultdict
import numpy as np
from sentence_transformers import SentenceTransformer

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import RAW_DIR, PROCESSED_DIR, MODEL_EMBEDDINGS

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
        "metadata": {"topics": article.get("topics", [])}
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
        "metadata": {"match_score": article.get("match_score")}
    }

def normaliser_rss(article):
    return {
        "article_id": generer_id(article.get("url"), article["title"], "rss"),
        "title": article["title"],
        "text": article.get("summary", ""),
        "source_name": "rss",
        "entreprise_cible": article["entreprise_cible"],
        "published_at": article.get("published_at", ""),
        "url": article.get("url"),
        "native_sentiment_score": None,
        "native_sentiment_label": None,
        "metadata": {}
    }

def marquer_confirmation_cross_source(articles, seuil=0.75):
    """Marque chaque article avec les sources qui parlent du même sujet (même entreprise, texte similaire)."""
    print("Calcul de la confirmation cross-source...")
    model = SentenceTransformer(MODEL_EMBEDDINGS)

    par_entreprise = defaultdict(list)
    for a in articles:
        par_entreprise[a["entreprise_cible"]].append(a)

    for entreprise, groupe in par_entreprise.items():
        if len(groupe) < 2:
            for a in groupe:
                a["confirmed_by_sources"] = [a["source_name"]]
            continue

        textes = [f"{a['title']} {a['text']}" for a in groupe]
        embeddings = model.encode(textes, show_progress_bar=False)

        for i, a in enumerate(groupe):
            sources_confirmantes = {a["source_name"]}
            for j, b in enumerate(groupe):
                if i == j or a["source_name"] == b["source_name"]:
                    continue
                sim = np.dot(embeddings[i], embeddings[j]) / (
                    np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[j])
                )
                if sim >= seuil:
                    sources_confirmantes.add(b["source_name"])
            a["confirmed_by_sources"] = sorted(sources_confirmantes)

    nb_confirmes = sum(1 for a in articles if len(a["confirmed_by_sources"]) > 1)
    print(f"Articles confirmés par plusieurs sources : {nb_confirmes} / {len(articles)}")
    return articles

def normaliser():
    tous_les_articles = []

    with open(RAW_DIR / "articles_alphavantage.json", "r", encoding="utf-8") as f:
        for a in json.load(f):
            tous_les_articles.append(normaliser_alphavantage(a))

    with open(RAW_DIR / "articles_marketaux.json", "r", encoding="utf-8") as f:
        for a in json.load(f):
            tous_les_articles.append(normaliser_marketaux(a))

    rss_path = RAW_DIR / "articles_rss.json"
    if rss_path.exists():
        with open(rss_path, "r", encoding="utf-8") as f:
            for a in json.load(f):
                tous_les_articles.append(normaliser_rss(a))

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

    articles_uniques = marquer_confirmation_cross_source(articles_uniques)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    output_path = PROCESSED_DIR / "articles_canonical.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(articles_uniques, f, ensure_ascii=False, indent=2)

    print(f"\nSauvegardé dans {output_path}")
    return articles_uniques

if __name__ == "__main__":
    normaliser()