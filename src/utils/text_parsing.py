import re

def extraire_label(reponse):
    match = re.search(r"Sentiment:\s*(\w+)", reponse, re.IGNORECASE)
    return match.group(1).lower() if match else "non_detecte"

def extraire_justification(reponse):
    match = re.search(r"Justification:\s*(.+)", reponse, re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else ""

def normaliser_label(label):
    """Uniformise les variantes (ex: 'mixed' -> 'neutral')"""
    return "neutral" if label == "mixed" else label


def normaliser_nom_critere(nom_critere):
    """Convertit un nom de critère type 'EvidenceGrounding' en 'evidence_grounding'.
    Garantit un nommage cohérent, peu importe le script qui génère l'évaluation."""
    return re.sub(r'(?<!^)(?=[A-Z])', '_', nom_critere).lower()

def extraire_champ(reponse, nom_champ):
    match = re.search(rf"{nom_champ}:\s*(.+)", reponse, re.IGNORECASE)
    return match.group(1).strip() if match else ""

def nettoyer_risques(texte):
    if texte.lower().startswith("aucun"):
        return "Aucun"
    return texte

def nettoyer_markdown(texte):
    return texte.replace("**", "").replace("*", "")