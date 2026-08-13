import json
import sys
from pathlib import Path
import ollama

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import PROCESSED_DIR, SENTIMENTS_DIR
from utils.text_parsing import extraire_label, extraire_justification, nettoyer_markdown
from config import MODEL_FINANCE_LLAMA


PROMPT_TEMPLATE = """Analyze the sentiment of this financial news article for investors.

Respond in this exact format, plain text only, no markdown:
Sentiment: [positive/negative/neutral]
Justification: [1-2 sentences explaining why]

Article: {texte}"""

def analyser_sentiment(texte):
    prompt = PROMPT_TEMPLATE.format(texte=texte)
    response = ollama.generate(model=MODEL_FINANCE_LLAMA, prompt=prompt)
    return response["response"]

def run(output_path=None):
    with open(PROCESSED_DIR / "articles_canonical.json", "r", encoding="utf-8") as f:
        articles = json.load(f)

    print(f"Traitement de {len(articles)} articles avec Finance-Llama-8B...")
    resultats = []
    output_path = output_path or (SENTIMENTS_DIR / "sentiment_financellama.json")
    SENTIMENTS_DIR.mkdir(parents=True, exist_ok=True)

    for i, article in enumerate(articles):
        texte = f"{article['title']} {article['text']}"
        reponse = nettoyer_markdown(analyser_sentiment(texte))

        resultats.append({
            "article_id": article["article_id"],
            "title": article["title"],
            "source_name": article["source_name"],
            "entreprise_cible": article["entreprise_cible"],
            "native_sentiment_label": article.get("native_sentiment_label"),
            "native_sentiment_score": article.get("native_sentiment_score"),
            "financellama_reponse": reponse,
            "financellama_label": extraire_label(reponse),
            "financellama_justification": extraire_justification(reponse),
            "text": article["text"]
        })

        print(f"  [{i + 1}/{len(articles)}] {article['entreprise_cible']} -> {resultats[-1]['financellama_label']}")

        if (i + 1) % 20 == 0:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(resultats, f, ensure_ascii=False, indent=2)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(resultats, f, ensure_ascii=False, indent=2)

    print(f"\nTerminé ! {len(resultats)} résultats sauvegardés dans {output_path}")
    return resultats

if __name__ == "__main__":
    run()