import json
import sys
from pathlib import Path
import ollama

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import PROCESSED_DIR, ENTITIES_DIR, MODEL_MISTRAL
from utils.text_parsing import extraire_champ, nettoyer_risques

PROMPT_TEMPLATE = """Extract information from this financial news article. Be extremely concise — a few words per field, not sentences.

Respond in this EXACT format, nothing else:
Entreprise: [company name, 1-4 words]
Secteur: [industry sector, 1-3 words]
Evenement: [event type, 1-4 words, e.g. "Share buyback", "Earnings report", "Merger"]
Risques: [main risk in 1-5 words, or "Aucun"]

Example:
Entreprise: Apple
Secteur: Technology
Evenement: Quarterly earnings
Risques: Supply chain disruption

Article: {texte}"""

def extraire_entites(texte):
    prompt = PROMPT_TEMPLATE.format(texte=texte)
    response = ollama.generate(model=MODEL_MISTRAL, prompt=prompt)
    reponse = response["response"]

    return {
        "entreprise_detectee": extraire_champ(reponse, "Entreprise"),
        "secteur": extraire_champ(reponse, "Secteur"),
        "evenement": extraire_champ(reponse, "Evenement"),
        "risques": nettoyer_risques(extraire_champ(reponse, "Risques"))
    }

def run():
    with open(PROCESSED_DIR / "articles_canonical.json", "r", encoding="utf-8") as f:
        articles = json.load(f)

    resultats = []
    print(f"Extraction d'entités sur {len(articles)} articles...")

    for i, article in enumerate(articles):
        entites = extraire_entites(f"{article['title']} {article['text']}")

        resultats.append({
            "article_id": article["article_id"],
            "title": article["title"],
            "source_name": article["source_name"],
            "entreprise_cible": article["entreprise_cible"],
            **entites
        })

        print(f"  [{i + 1}/{len(articles)}] {article['entreprise_cible']} -> {entites['secteur']} / {entites['evenement']}")

        if (i + 1) % 20 == 0:
            with open(ENTITIES_DIR / "entities_mistral.json", "w", encoding="utf-8") as f:
                json.dump(resultats, f, ensure_ascii=False, indent=2)

    ENTITIES_DIR.mkdir(parents=True, exist_ok=True)
    output_path = ENTITIES_DIR / "entities_mistral.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(resultats, f, ensure_ascii=False, indent=2)

    print(f"\nTerminé ! Sauvegardé dans {output_path}")
    return resultats

if __name__ == "__main__":
    run()