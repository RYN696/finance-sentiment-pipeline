import json
import re
import sys
from pathlib import Path
import ollama

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import EVALUATION_DIR, PROCESSED_DIR, MODEL_QWEN_JUDGE

CRITERES = ["Faithfulness", "Relevance", "Completeness", "Clarity", "Hallucination", "Consistency", "EvidenceGrounding"]

def evaluer_justification(texte, label, justification):
    prompt = f"""You are a neutral expert evaluator of financial sentiment justifications.

    Article: {texte}
    Predicted sentiment: {label}
    Justification: {justification}

    Rate the justification from 1 (very poor) to 5 (excellent).

    Evaluate ONLY the quality of the justification based on the article. Apply the same standards to every justification, regardless of how it was generated.

    - Faithfulness: Is it factually accurate and free of unsupported claims?
    - Relevance: Does it focus on the most important information supporting the sentiment?
    - Completeness: Does it cover the main reasons supporting the sentiment?
    - Clarity: Is it clear, concise, and well written?
    - Hallucination: 5 = no invented or unsupported information; 1 = clearly invented information.
    - Consistency: Does it logically support the predicted sentiment?
    - EvidenceGrounding: Does it use specific facts from the article rather than vague statements?

    Respond ONLY in this format:
    Faithfulness: [score]
    Relevance: [score]
    Completeness: [score]
    Clarity: [score]
    Hallucination: [score]
    Consistency: [score]
    EvidenceGrounding: [score]"""

    response = ollama.generate(model=MODEL_QWEN_JUDGE, prompt=prompt)
    return response["response"]

def extraire_scores(reponse):
    scores = {}
    for critere in CRITERES:
        match = re.search(rf"{critere}:\s*(\d)", reponse, re.IGNORECASE)
        scores[critere] = int(match.group(1)) if match else None
    return scores

def run(justifications_path, label_key, justification_key, output_path, text_key="text", need_join=False, max_articles=None):
    with open(justifications_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if max_articles:
        data = data[:max_articles]

    texte_par_id = {}
    if need_join:
        with open(PROCESSED_DIR / "articles_canonical.json", "r", encoding="utf-8") as f:
            articles = json.load(f)
        texte_par_id = {a["article_id"]: f"{a['title']} {a['text']}" for a in articles}

    resultats = []
    EVALUATION_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Évaluation de {len(data)} justifications ({justifications_path.name})...")

    for i, article in enumerate(data):
        texte = texte_par_id.get(article.get("article_id")) if need_join else article.get(text_key, "")

        reponse = evaluer_justification(texte, article[label_key], article[justification_key])
        scores = extraire_scores(reponse)

        resultats.append({
            "article_id": article.get("article_id"),
            "title": article["title"],
            "source_name": article.get("source_name"),
            "entreprise_cible": article["entreprise_cible"],
            "label": article[label_key],
            "justification": article[justification_key],
            **{k.lower(): v for k, v in scores.items()}
        })

        if (i + 1) % 20 == 0:
            print(f"  {i + 1}/{len(data)} évalués...")
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(resultats, f, ensure_ascii=False, indent=2)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(resultats, f, ensure_ascii=False, indent=2)

    print(f"Terminé ! Sauvegardé dans {output_path}")
    return resultats