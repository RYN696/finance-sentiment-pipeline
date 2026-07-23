import json
import re

with open("data/results/resultats_mistral.json", "r", encoding="utf-8") as f:
    resultats = json.load(f)

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

for r in resultats:
    r["mistral_label"] = extraire_label(r["mistral_reponse"])
    r["mistral_justification"] = extraire_justification(r["mistral_reponse"])

# Vérifier combien n'ont pas été détectés correctement
non_detectes = sum(1 for r in resultats if r["mistral_label"] == "non_detecte")
print(f"Labels non détectés : {non_detectes} / {len(resultats)}")

# Répartition des labels
from collections import Counter
compteur = Counter(r["mistral_label"] for r in resultats)
print("\nRépartition des sentiments Mistral :")
for label, count in compteur.items():
    print(f"  {label} : {count}")

with open("data/results/resultats_mistral_propres.json", "w", encoding="utf-8") as f:
    json.dump(resultats, f, ensure_ascii=False, indent=2)

print("\nSauvegardé dans data/results/resultats_mistral_propres.json")