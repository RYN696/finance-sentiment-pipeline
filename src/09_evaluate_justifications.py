import json
import re
import ollama

with open("data/results/finbert_justifications.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def evaluer_justification(summary, label, justification):
    prompt = f"""You are an expert evaluator assessing the quality of a sentiment justification for a financial news article.

Article summary: {summary}
Predicted sentiment label: {label}
Justification given: {justification}

Rate the justification from 1 (very poor) to 5 (excellent) on each of the following criteria:

- Faithfulness: does the justification accurately reflect the article, without inventing facts?
- Relevance: does it focus on the most important information related to the sentiment?
- Completeness: does it cover the key reasons behind the sentiment, not just a partial view?
- Clarity: is it easy to understand and well written?
- Hallucination: rate 5 if there is NO invented/false information, 1 if it contains clearly invented information.
- Consistency with the predicted sentiment: does the justification logically support the label "{label}" without contradicting it?
- Evidence Grounding: does it reference specific facts/details from the article, rather than vague generic statements?

Respond ONLY in this exact format, nothing else, no explanations:
Faithfulness: [score]
Relevance: [score]
Completeness: [score]
Clarity: [score]
Hallucination: [score]
Consistency: [score]
EvidenceGrounding: [score]"""

    response = ollama.generate(model="qwen2.5:14b", prompt=prompt)
    return response["response"]

def extraire_scores(reponse):
    criteres = ["Faithfulness", "Relevance", "Completeness", "Clarity", "Hallucination", "Consistency", "EvidenceGrounding"]
    scores = {}
    for critere in criteres:
        match = re.search(rf"{critere}:\s*(\d)", reponse, re.IGNORECASE)
        scores[critere] = int(match.group(1)) if match else None
    return scores

resultats = []

print(f"Évaluation de {len(data)} articles avec Qwen 2.5...")

for i, article in enumerate(data):
    reponse = evaluer_justification(article["summary"], article["finbert_label"], article["finbert_justification"])
    scores = extraire_scores(reponse)

    resultats.append({
        "entreprise_cible": article["entreprise_cible"],
        "title": article["title"],
        "finbert_label": article["finbert_label"],
        "finbert_justification": article["finbert_justification"],
        "faithfulness": scores["Faithfulness"],
        "relevance": scores["Relevance"],
        "completeness": scores["Completeness"],
        "clarity": scores["Clarity"],
        "hallucination": scores["Hallucination"],
        "consistency": scores["Consistency"],
        "evidence_grounding": scores["EvidenceGrounding"]
    })

    if (i + 1) % 20 == 0:
        print(f"  {i + 1}/{len(data)} articles évalués...")
        with open("data/results/evaluation_justifications.json", "w", encoding="utf-8") as f:
            json.dump(resultats, f, ensure_ascii=False, indent=2)

with open("data/results/evaluation_justifications.json", "w", encoding="utf-8") as f:
    json.dump(resultats, f, ensure_ascii=False, indent=2)

print(f"\nTerminé ! {len(resultats)} évaluations sauvegardées dans data/results/evaluation_justifications.json")