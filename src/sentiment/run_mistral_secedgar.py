import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import PROCESSED_DIR, SENTIMENTS_DIR, MODEL_MISTRAL
from sentiment.run_mistral import analyser_sentiment
from utils.text_parsing import extraire_label, extraire_justification

def run():
    input_path = PROCESSED_DIR / "secedgar_prepares.json"
    with open(input_path, "r", encoding="utf-8") as f:
        articles = json.load(f)

    resultats = []
    print(f"Traitement de {len(articles)} documents SEC EDGAR avec Mistral...")

    for i, article in enumerate(articles):
        texte = f"{article['title']} {article['summary']}"
        reponse = analyser_sentiment(texte)

        resultats.append({
            "entreprise_cible": article["entreprise_cible"],
            "title": article["title"],
            "mistral_label": extraire_label(reponse),
            "mistral_justification": extraire_justification(reponse)
        })

        print(f"  [{i + 1}/{len(articles)}] {article['entreprise_cible']} -> {resultats[-1]['mistral_label']}")

    output_path = SENTIMENTS_DIR / "sentiment_mistral_secedgar.json"
    SENTIMENTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(resultats, f, ensure_ascii=False, indent=2)

    print(f"Terminé ! Sauvegardé dans {output_path}")
    return resultats

if __name__ == "__main__":
    run()