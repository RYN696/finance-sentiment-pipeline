import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import RAW_DIR, PROCESSED_DIR

def extraire_titre(texte, longueur=100):
    """Prend les premières lignes comme titre approximatif."""
    lignes = [l.strip() for l in texte.split("\n") if l.strip()]
    return lignes[0][:longueur] if lignes else "Sans titre"

def preparer():
    input_path = RAW_DIR / "secedgar_8k.json"
    with open(input_path, "r", encoding="utf-8") as f:
        documents = json.load(f)

    articles_formates = []
    for doc in documents:
        articles_formates.append({
            "entreprise_cible": doc["entreprise_cible"],
            "title": extraire_titre(doc["texte"]),
            "summary": doc["texte"][:1000],
            "source": "SEC_EDGAR",
            "filing_date": doc["filing_date"]
        })

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    output_path = PROCESSED_DIR / "secedgar_prepares.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(articles_formates, f, ensure_ascii=False, indent=2)

    print(f"{len(articles_formates)} documents formatés sauvegardés dans {output_path}")
    return articles_formates

if __name__ == "__main__":
    preparer()