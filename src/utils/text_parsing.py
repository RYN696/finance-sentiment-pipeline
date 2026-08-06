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