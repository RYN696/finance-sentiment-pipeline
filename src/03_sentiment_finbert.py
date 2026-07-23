import json
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

print("Chargement du modèle FinBERT ")

MODEL_NAME = "ProsusAI/finbert"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
model.eval()

labels = ["positive", "negative", "neutral"]

def analyser_sentiment(texte):
    inputs = tokenizer(texte, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    scores = torch.nn.functional.softmax(outputs.logits, dim=1)[0]
    scores = scores.tolist()
    resultat = {labels[i]: round(scores[i], 4) for i in range(len(labels))}
    label_final = labels[scores.index(max(scores))]
    return label_final, resultat

# Charger les articles préparés
with open("data/processed/articles_prepares.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

print(f"Analyse de {len(articles)} articles avec FinBERT...")

resultats = []
for i, article in enumerate(articles):
    texte = f"{article['title']} {article['summary']}"
    label, scores = analyser_sentiment(texte)

    resultats.append({
        "entreprise_cible": article["entreprise_cible"],
        "title": article["title"],
        "alphavantage_label": article.get("overall_sentiment_label"),
        "alphavantage_score": article.get("overall_sentiment_score"),
        "finbert_label": label,
        "finbert_positive": scores["positive"],
        "finbert_negative": scores["negative"],
        "finbert_neutral": scores["neutral"]
    })

    if (i + 1) % 50 == 0:
        print(f"  {i + 1}/{len(articles)} articles traités...")

df_resultats = pd.DataFrame(resultats)
df_resultats.to_json("data/results/resultats_finbert.json", orient="records", force_ascii=False, indent=2)

print(f"\nTerminé ! Résultats sauvegardés dans data/results/resultats_finbert.json")
print("\nAperçu :")
print(df_resultats[["entreprise_cible", "alphavantage_label", "finbert_label"]].head(10))