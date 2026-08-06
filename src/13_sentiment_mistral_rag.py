import json
import re
import numpy as np
import ollama
from sentence_transformers import SentenceTransformer

# Charger la banque (avec embeddings) et le test set
with open("data/processed/rag_banque.json", "r", encoding="utf-8") as f:
    banque = json.load(f)

with open("data/processed/rag_test_set.json", "r", encoding="utf-8") as f:
    test_set = json.load(f)

print(f"Banque de référence : {len(banque)} articles")
print(f"Ensemble de test : {len(test_set)} articles")

# Charger le modèle d'embeddings (même modèle que pour la banque)
print("Chargement du modèle d'embeddings...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Préparer les embeddings de la banque sous forme de matrice numpy
embeddings_banque = np.array([a["embedding"] for a in banque])

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def trouver_exemples_similaires(texte_article, k=4):
    embedding_article = model.encode([texte_article])[0]
    similarites = [cosine_similarity(embedding_article, emb) for emb in embeddings_banque]
    indices_tries = np.argsort(similarites)[::-1][:k]
    return [banque[i] for i in indices_tries]

def construire_bloc_exemples(exemples):
    bloc = ""
    for ex in exemples:
        bloc += f'Article: "{ex["title"]} {ex["summary"]}"\nSentiment: {ex["api_label_normalise"]}\n\n'
    return bloc

def analyser_sentiment(texte, exemples):
    bloc_exemples = construire_bloc_exemples(exemples)
    prompt = f"""You are a financial analyst classifying the sentiment of a news article for investors, following the same classification logic as a professional financial data provider.

Here are similar real examples with their correct sentiment classification:

{bloc_exemples}
Now classify the following article using the SAME logic and level of strictness as shown in the examples above.

Respond in this exact format:
Sentiment: [positive/negative/neutral]
Justification: [1-2 sentences explaining why]

Article: {texte}"""

    response = ollama.generate(model="mistral", prompt=prompt)
    return response["response"]

def extraire_label(reponse):
    match = re.search(r"Sentiment:\s*(\w+)", reponse, re.IGNORECASE)
    return match.group(1).lower() if match else "non_detecte"

def extraire_justification(reponse):
    match = re.search(r"Justification:\s*(.+)", reponse, re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else ""

resultats = []

print(f"\nTraitement de {len(test_set)} articles avec Mistral + RAG...")

for i, article in enumerate(test_set):
    texte = f"{article['title']} {article['summary']}"
    exemples = trouver_exemples_similaires(texte, k=4)
    reponse = analyser_sentiment(texte, exemples)
    label = extraire_label(reponse)
    justification = extraire_justification(reponse)

    resultats.append({
        "entreprise_cible": article["entreprise_cible"],
        "title": article["title"],
        "summary": article["summary"],
        "api_label_normalise": article["api_label_normalise"],
        "mistral_reponse": reponse,
        "mistral_label": label,
        "mistral_justification": justification
    })

    print(f"  [{i + 1}/{len(test_set)}] {article['entreprise_cible']} -> {label} (API: {article['api_label_normalise']})")

    if (i + 1) % 20 == 0:
        with open("data/results/resultats_mistral_rag.json", "w", encoding="utf-8") as f:
            json.dump(resultats, f, ensure_ascii=False, indent=2)

with open("data/results/resultats_mistral_rag.json", "w", encoding="utf-8") as f:
    json.dump(resultats, f, ensure_ascii=False, indent=2)

print(f"\nTerminé ! {len(resultats)} résultats sauvegardés dans data/results/resultats_mistral_rag.json")