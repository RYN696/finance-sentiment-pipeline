import json
import random
from sentence_transformers import SentenceTransformer

random.seed(42)  # pour reproductibilité

with open("data/processed/articles_prepares.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

print(f"Nombre total d'articles : {len(articles)}")

# Convertir le label API en 3 catégories (comme avant)
def convertir_alphavantage(label):
    if label in ["Bullish", "Somewhat-Bullish"]:
        return "positive"
    elif label in ["Bearish", "Somewhat-Bearish"]:
        return "negative"
    else:
        return "neutral"

for a in articles:
    a["api_label_normalise"] = convertir_alphavantage(a.get("overall_sentiment_label", "Neutral"))

# Mélanger et séparer : ~150 pour la banque, le reste pour le test
random.shuffle(articles)
taille_banque = 150
banque = articles[:taille_banque]
test_set = articles[taille_banque:]

print(f"Banque de référence : {len(banque)} articles")
print(f"Ensemble de test : {len(test_set)} articles")

# Charger le modèle d'embeddings (léger, local)
print("\nChargement du modèle d'embeddings...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Générer les embeddings pour la banque
textes_banque = [f"{a['title']} {a['summary']}" for a in banque]
embeddings = model.encode(textes_banque, show_progress_bar=True)

for i, a in enumerate(banque):
    a["embedding"] = embeddings[i].tolist()

# Sauvegarder
with open("data/processed/rag_banque.json", "w", encoding="utf-8") as f:
    json.dump(banque, f, ensure_ascii=False)

with open("data/processed/rag_test_set.json", "w", encoding="utf-8") as f:
    json.dump(test_set, f, ensure_ascii=False, indent=2)

print("\nSauvegardé : data/processed/rag_banque.json et data/processed/rag_test_set.json")