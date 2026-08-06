import json
import sys
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import ARTICLES_PREPARES, RESULTATS_FINBERT, SENTIMENTS_DIR

LABELS = ["positive", "negative", "neutral"]

def charger_modele():
    print("Chargement du modèle FinBERT...")
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
    model.eval()
    return tokenizer, model

def analyser_sentiment(texte, tokenizer, model):
    inputs = tokenizer(texte, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    scores = torch.nn.functional.softmax(outputs.logits, dim=1)[0].tolist()
    resultat = {LABELS[i]: round(scores[i], 4) for i in range(len(LABELS))}
    label_final = LABELS[scores.index(max(scores))]
    return label_final, resultat

def run(output_path=None):
    tokenizer, model = charger_modele()

    with open(ARTICLES_PREPARES, "r", encoding="utf-8") as f:
        articles = json.load(f)

    print(f"Analyse de {len(articles)} articles avec FinBERT...")
    resultats = []

    for i, article in enumerate(articles):
        texte = f"{article['title']} {article['summary']}"
        label, scores = analyser_sentiment(texte, tokenizer, model)

        resultats.append({
            "entreprise_cible": article["entreprise_cible"],
            "title": article["title"],
            "alphavantage_label": article.get("overall_sentiment_label"),
            "finbert_label": label,
            "finbert_positive": scores["positive"],
            "finbert_negative": scores["negative"],
            "finbert_neutral": scores["neutral"]
        })

        if (i + 1) % 50 == 0:
            print(f"  {i + 1}/{len(articles)} articles traités...")

    output_path = output_path or RESULTATS_FINBERT
    SENTIMENTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(resultats, f, ensure_ascii=False, indent=2)

    print(f"\nTerminé ! Résultats sauvegardés dans {output_path}")
    return resultats

if __name__ == "__main__":
    run()