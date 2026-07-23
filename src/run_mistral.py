import json
import ollama

with open("data/articles_prepares.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

def analyser_sentiment(texte):
    prompt = f"""Analyze the sentiment of this financial news article. 
Respond in this exact format:
Sentiment: [positive/negative/neutral]
Justification: [1-2 sentences explaining why]

Article: {texte}"""

    response = ollama.generate(model="mistral", prompt=prompt)
    return response["response"]

resultats = []

print(f"Traitement de {len(articles)} articles avec Mistral...")

for i, article in enumerate(articles):
    texte = f"{article['title']} {article['summary']}"
    reponse = analyser_sentiment(texte)

    resultats.append({
        "entreprise_cible": article["entreprise_cible"],
        "title": article["title"],
        "alphavantage_label": article.get("overall_sentiment_label"),
        "mistral_reponse": reponse
    })

    if (i + 1) % 20 == 0:
        print(f"  {i + 1}/{len(articles)} articles traités...")
        # Sauvegarde intermédiaire, au cas où
        with open("data/resultats_mistral.json", "w", encoding="utf-8") as f:
            json.dump(resultats, f, ensure_ascii=False, indent=2)

# Sauvegarde finale
with open("data/resultats_mistral.json", "w", encoding="utf-8") as f:
    json.dump(resultats, f, ensure_ascii=False, indent=2)

print(f"\nTerminé ! {len(resultats)} résultats sauvegardés dans data/resultats_mistral.json")