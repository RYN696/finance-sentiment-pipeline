import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import PROCESSED_DIR, SENTIMENTS_DIR
from sentiment.run_mistral import analyser_sentiment
from utils.text_parsing import extraire_label, extraire_justification

def run():
    input_path = PROCESSED_DIR / "marketaux_prepares.json"
    with open(input_path, "r", encoding="utf-8") as f:
        articles = json.load(f)

    resultats = []
    print(f"Traitement de {len(articles)} articles Marketaux avec Mistral...")

    for i, article in enumerate(articles):
        texte = f"{article['title']} {article['summary']}"
        reponse = analyser_sentiment(texte)

        resultats.append({
        "entreprise_cible": article["entreprise_cible"],
        "title": article["title"],
        "summary": article["summary"],
        "mistral_label": extraire_label(reponse),
        "mistral_justification": extraire_justification(reponse)
        })

        print(f"  [{i + 1}/{len(articles)}] {article['entreprise_cible']} -> {resultats[-1]['mistral_label']}")

    SENTIMENTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = SENTIMENTS_DIR / "sentiment_mistral_marketaux.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(resultats, f, ensure_ascii=False, indent=2)

    print(f"Terminé ! Sauvegardé dans {output_path}")
    return resultats

if __name__ == "__main__":
    run()