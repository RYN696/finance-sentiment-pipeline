import json
import sys
from pathlib import Path
import ollama

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import RESULTATS_FINBERT, FINBERT_JUSTIFICATIONS, JUSTIFICATIONS_DIR, PROCESSED_DIR, MODEL_MISTRAL

def justifier_sentiment(texte, label):
    prompt = f"""FinBERT classified this financial news article as "{label}".
Explain in 1-2 sentences, in English only, why this sentiment is consistent with the article's content.
Respond only with the justification in English, without repeating the label.

Article: {texte}"""
    response = ollama.generate(model=MODEL_MISTRAL, prompt=prompt)
    return response["response"].strip()

def run(finbert_results_path=None, articles_path=None, output_path=None):
    finbert_results_path = finbert_results_path or RESULTATS_FINBERT
    articles_path = articles_path or (PROCESSED_DIR / "articles_canonical.json")
    output_path = output_path or FINBERT_JUSTIFICATIONS

    with open(finbert_results_path, "r", encoding="utf-8") as f:
        finbert_data = json.load(f)
    with open(articles_path, "r", encoding="utf-8") as f:
        articles = json.load(f)

    texte_par_id = {a["article_id"]: f"{a['title']} {a['text']}" for a in articles}

    resultats = []
    JUSTIFICATIONS_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Génération de justifications pour {len(finbert_data)} articles FinBERT...")

    for i, article in enumerate(finbert_data):
        texte = texte_par_id.get(article["article_id"], article["title"])
        justification = justifier_sentiment(texte, article["finbert_label"])

        resultats.append({
            "article_id": article["article_id"],
            "title": article["title"],
            "source_name": article["source_name"],
            "entreprise_cible": article["entreprise_cible"],
            "native_sentiment_label": article.get("native_sentiment_label"),
            "native_sentiment_score": article.get("native_sentiment_score"),
            "finbert_label": article["finbert_label"],
            "finbert_justification": justification,
            "text": texte_par_id.get(article["article_id"], "")
        })

        if (i + 1) % 20 == 0:
            print(f"  {i + 1}/{len(finbert_data)} articles traités...")
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(resultats, f, ensure_ascii=False, indent=2)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(resultats, f, ensure_ascii=False, indent=2)

    print(f"\nTerminé ! {len(resultats)} justifications sauvegardées dans {output_path}")
    return resultats

if __name__ == "__main__":
    run()