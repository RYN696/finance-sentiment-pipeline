import json
import sys
from pathlib import Path
import ollama

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import ARTICLES_PREPARES, RESULTATS_MISTRAL, SENTIMENTS_DIR, MODEL_MISTRAL
from utils.text_parsing import extraire_label, extraire_justification

PROMPT_TEMPLATE = """You are a financial analyst classifying the sentiment of a news article for investors.

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

def analyser_sentiment(texte):
    prompt = PROMPT_TEMPLATE.format(texte=texte)
    response = ollama.generate(model=MODEL_MISTRAL, prompt=prompt)
    return response["response"]

def run(output_path=None):
    with open(ARTICLES_PREPARES, "r", encoding="utf-8") as f:
        articles = json.load(f)

    print(f"Traitement de {len(articles)} articles avec Mistral...")
    resultats = []
    output_path = output_path or RESULTATS_MISTRAL
    SENTIMENTS_DIR.mkdir(parents=True, exist_ok=True)

    for i, article in enumerate(articles):
        texte = f"{article['title']} {article['summary']}"
        reponse = analyser_sentiment(texte)

        resultats.append({
            "entreprise_cible": article["entreprise_cible"],
            "title": article["title"],
            "alphavantage_label": article.get("overall_sentiment_label"),
            "mistral_reponse": reponse,
            "mistral_label": extraire_label(reponse),
            "mistral_justification": extraire_justification(reponse)
        })

        print(f"  [{i + 1}/{len(articles)}] {article['entreprise_cible']} -> {resultats[-1]['mistral_label']}")

        if (i + 1) % 20 == 0:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(resultats, f, ensure_ascii=False, indent=2)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(resultats, f, ensure_ascii=False, indent=2)

    print(f"\nTerminé ! {len(resultats)} résultats sauvegardés dans {output_path}")
    return resultats

if __name__ == "__main__":
    run()