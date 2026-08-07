import json
import sys
from pathlib import Path
from edgar import Company, set_identity

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import RAW_DIR

set_identity("Rayen rayen.ghrairi@esprit.tn")

ENTREPRISES = {
    "Apple": "AAPL", "Microsoft": "MSFT", "Amazon": "AMZN",
    "Tesla": "TSLA", "Google": "GOOGL", "Meta": "META",
    "Nvidia": "NVDA", "JPMorgan": "JPM", "Johnson & Johnson": "JNJ"
}

def extraire_texte_exhibit(filing):
    """Cherche l'exhibit 99.1 (communiqué de presse réel), sinon retombe sur le document principal."""
    try:
        for att in filing.attachments:
            if "ex99" in str(att.document).lower():
                return att.text()
    except Exception:
        pass

    try:
        return filing.text()
    except Exception:
        return None

def collecter_8k_entreprise(ticker, nb_filings=5):
    company = Company(ticker)
    filings = company.get_filings(form="8-K").head(nb_filings)

    documents = []
    for filing in filings:
        texte = extraire_texte_exhibit(filing)
        if not texte:
            continue

        documents.append({
            "ticker": ticker,
            "form_type": "8-K",
            "filing_date": str(filing.filing_date),
            "texte": texte[:3000]  # on limite la longueur pour rester cohérent avec vos autres articles
        })

    return documents

def collecter():
    tous_les_documents = []

    for entreprise, ticker in ENTREPRISES.items():
        print(f"Collecte pour {entreprise} ({ticker})...")
        documents = collecter_8k_entreprise(ticker)

        for doc in documents:
            doc["entreprise_cible"] = entreprise
            tous_les_documents.append(doc)

        print(f"  {len(documents)} documents récupérés")

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RAW_DIR / "secedgar_8k.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(tous_les_documents, f, ensure_ascii=False, indent=2)

    print(f"\nTotal : {len(tous_les_documents)} documents sauvegardés dans {output_path}")
    return tous_les_documents

if __name__ == "__main__":
    collecter()