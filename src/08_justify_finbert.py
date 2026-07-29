import json
import re
import ollama

with open("data/results/resultats_finbert.json", "r", encoding="utf-8") as f:
    finbert_data = json.load(f)

with open("data/processed/articles_prepares.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

# Dictionnaire pour retrouver rapidement le texte de chaque article par son titre
textes_par_titre = {a["title"]: f"{a['title']} {a['summary']}" for a in articles}

def justifier_sentiment(texte, label):
    prompt = f"""You are writing a short explanation for a financial sentiment classification system.
Rules you MUST follow:
- Start your answer directly with the actual reason .
- Do not mention the word "{label}" anywhere in your answer.
- Write exactly 1-2 sentences in English.

Article: {texte}

Write only the explanation, following the rules above:"""

    response = ollama.generate(model="mistral", prompt=prompt)
    return response["response"].strip()

def nettoyer_justification(texte, label):
    texte = re.sub(
        rf"^(this is |the sentiment (of |is )?)?\"?{label}\"?[\s,:-]*\s*(because|as|since)?\s*",
        "",
        texte,
        flags=re.IGNORECASE
    )
    return texte.strip().capitalize()

resultats = []

print(f"Traitement de {len(finbert_data)} articles...")

for i, article in enumerate(finbert_data):
    texte = textes_par_titre.get(article["title"], article["title"])
    label = article["finbert_label"]

    justification = justifier_sentiment(texte, label)
    justification = nettoyer_justification(justification, label)

    resultats.append({
        "entreprise_cible": article["entreprise_cible"],
        "title": article["title"],
        "finbert_label": label,
        "finbert_justification": justification
    })

    if (i + 1) % 20 == 0:
        print(f"  {i + 1}/{len(finbert_data)} articles traités...")
        with open("data/results/finbert_justifications.json", "w", encoding="utf-8") as f:
            json.dump(resultats, f, ensure_ascii=False, indent=2)

with open("data/results/finbert_justifications.json", "w", encoding="utf-8") as f:
    json.dump(resultats, f, ensure_ascii=False, indent=2)

print(f"\nTerminé ! {len(resultats)} justifications sauvegardées dans data/results/finbert_justifications.json")