import json
import re
import ollama

with open("data/processed/articles_prepares.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

def analyser_sentiment(texte):
    prompt = f"""You are a financial analyst classifying the sentiment of a news article for investors.

Rules:
- Use "neutral" ONLY if the article truly contains no meaningful positive or negative financial signal (e.g. purely factual disclosures with no impact).
- If the article contains ANY positive financial signal (earnings beat, dividend increase, buy rating, expansion, growth, contract win), classify it as "positive", even if mentioned alongside neutral information.
- If the article contains ANY negative financial signal (cuts, losses, impairment, downgrade, missed expectations), classify it as "negative", even if the company frames it positively.
- Do not soften your classification just because the company uses reassuring language. Focus on the actual financial facts.
- Avoid defaulting to "neutral" as a safe choice — only use it when truly justified.

Respond in this exact format:
Sentiment: [positive/negative/neutral]
Justification: [1-2 sentences explaining why]

Article: {texte}"""

    response = ollama.generate(model="mistral", prompt=prompt)
    return response["response"]

def extraire_label(reponse):
    match = re.search(r"Sentiment:\s*(\w+)", reponse, re.IGNORECASE)
    if match:
        return match.group(1).lower()
    return "non_detecte"

def extraire_justification(reponse):
    match = re.search(r"Justification:\s*(.+)", reponse, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

resultats = []

print(f"Traitement de {len(articles)} articles avec le nouveau prompt...")

for i, article in enumerate(articles):
    texte = f"{article['title']} {article['summary']}"
    reponse = analyser_sentiment(texte)
    label = extraire_label(reponse)
    justification = extraire_justification(reponse)

    resultats.append({
        "entreprise_cible": article["entreprise_cible"],
        "title": article["title"],
        "alphavantage_label": article.get("overall_sentiment_label"),
        "mistral_reponse": reponse,
        "mistral_label": label,
        "mistral_justification": justification
    })

    print(f"  [{i + 1}/{len(articles)}] {article['entreprise_cible']} -> {label}")

    if (i + 1) % 20 == 0:
        with open("data/results/resultats_mistral.json", "w", encoding="utf-8") as f:
            json.dump(resultats, f, ensure_ascii=False, indent=2)

with open("data/results/resultats_mistral.json", "w", encoding="utf-8") as f:
    json.dump(resultats, f, ensure_ascii=False, indent=2)

print(f"\nTerminé ! {len(resultats)} résultats sauvegardés dans data/results/resultats_mistral.json")