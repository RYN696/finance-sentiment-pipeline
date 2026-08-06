import json
import sys
from pathlib import Path
import ollama

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import RESULTATS_FINBERT, ARTICLES_PREPARES, FINBERT_JUSTIFICATIONS, JUSTIFICATIONS_DIR, MODEL_MISTRAL

"""
Ce script génère une justification a posteriori pour les sentiments FinBERT.
Contrairement à Mistral (qui génère nativement label + justification dans sa réponse),
FinBERT est un classifieur pur sans capacité de génération de texte — 
une justification doit donc être produite séparément par un LLM (Mistral).
"""

def justifier_sentiment(texte, label):
    prompt = f"""FinBERT classified this financial news article as "{label}".
Explain in 1-2 sentences, in English only, why this sentiment is consistent with the article's content.
Respond only with the justification in English, without repeating the label.

Article: {texte}"""
    response = ollama.generate(model=MODEL_MISTRAL, prompt=prompt)
    return response["response"].strip()

def run(finbert_results_path=None, articles_path=None, output_path=None):
    finbert_results_path = finbert_results_path or RESULTATS_FINBERT
    articles_path = articles_path or ARTICLES_PREPARES
    output_path = output_path or FINBERT_JUSTIFICATIONS

    with open(finbert_results_path, "r", encoding="utf-8") as f:
        finbert_data = json.load(f)
    with open(articles_path, "r", encoding="utf-8") as f:
        articles = json.load(f)

    textes_par_titre = {a["title"]: f"{a['title']} {a['summary']}" for a in articles}
    summary_par_titre = {a["title"]: a["summary"] for a in articles}

    resultats = []
    JUSTIFICATIONS_DIR.mkdir(parents=True, exist_ok=True)

    for i, article in enumerate(finbert_data):
        texte = textes_par_titre.get(article["title"], article["title"])
        justification = justifier_sentiment(texte, article["finbert_label"])

        resultats.append({
            "entreprise_cible": article["entreprise_cible"],
            "title": article["title"],
            "finbert_label": article["finbert_label"],
            "finbert_justification": justification,
            "summary": summary_par_titre.get(article["title"], "")
        })

        if (i + 1) % 20 == 0:
            print(f"  {i + 1}/{len(finbert_data)} articles traités...")
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(resultats, f, ensure_ascii=False, indent=2)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(resultats, f, ensure_ascii=False, indent=2)

    print(f"Terminé ! Sauvegardé dans {output_path}")
    return resultats

if __name__ == "__main__":
    run()