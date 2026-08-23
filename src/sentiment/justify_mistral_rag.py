import json
import sys
from pathlib import Path
import ollama

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import SENTIMENTS_DIR, PROCESSED_DIR, MODEL_MISTRAL, JUSTIFICATIONS_DIR
from rag.retrieval import rechercher_passages_similaires

PROMPT_TEMPLATE = """You are a financial analyst writing a concise justification for a sentiment classification.

Sentiment classification: {label}

MAIN ARTICLE:
{texte}

RETRIEVED EVIDENCE:
The following passages were retrieved using semantic similarity.
They are ordered from most similar to least similar to the main article:
- Evidence 1 is the most similar passage.
- Evidence 2 is the second most similar passage.
- Evidence 3 is the third most similar passage.
- Evidence 4 is the fourth most similar passage.
- Evidence 5 is the fifth most similar passage.

{evidence}

Your task is to write a 2-3 sentence justification explaining why the given sentiment is supported by the MAIN ARTICLE.

IMPORTANT RULES:
1. The MAIN ARTICLE is the primary source and the main basis for your justification.
2. The retrieved evidence is supplementary information that can improve the justification when it is relevant.
3. Evaluate the relevance of each evidence passage before using it.
4. Use an evidence passage only if it directly supports, clarifies, or provides useful context for information in the main article.
5. Evidence 1 is the most semantically similar passage, but do not assume that it is automatically the most useful evidence.
6. You do NOT need to use every evidence passage.
7. Ignore evidence that is irrelevant, redundant, ambiguous, outdated, or contradictory to the main article.
8. Do not force information from the evidence into the justification.
9. Do not replace information from the main article with information from the retrieved evidence.
10. Do not invent or infer facts that are not supported by the main article or relevant evidence.
11. Focus on concrete financial factors, events, results, trends, or indicators that explain the sentiment.
12. Do not simply repeat the sentiment label.
13. The final justification must remain consistent with the information in the main article.

Before writing the justification, identify the most useful information from the main article and determine whether any retrieved evidence adds relevant supporting or contextual information.

Respond in exactly this format:
Justification: [2-3 concise sentences]"""

def construire_bloc_evidence(passages):
    if not passages:
        return "No additional evidence found."
    return "\n".join(f"- {p['chunk_text']}" for p in passages)

def generer_justification_rag(texte, label, entreprise_cible):
    passages = rechercher_passages_similaires(texte, entreprise_cible=entreprise_cible, k=5)
    evidence = construire_bloc_evidence(passages)

    prompt = PROMPT_TEMPLATE.format(label=label, texte=texte, evidence=evidence)
    response = ollama.generate(model=MODEL_MISTRAL, prompt=prompt)
    return response["response"], passages

def run(input_path=None, output_path=None):
    input_path = input_path or ( JUSTIFICATIONS_DIR / "mistral_justifications.json")
    output_path = output_path or (JUSTIFICATIONS_DIR / "mistral_justifications_rag.json")

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(PROCESSED_DIR / "articles_canonical.json", "r", encoding="utf-8") as f:
        articles = json.load(f)
    texte_par_id = {a["article_id"]: f"{a['title']} {a['text']}" for a in articles}

    resultats = []
    print(f"Génération de justifications RAG pour {len(data)} articles (Mistral)...")

    for i, article in enumerate(data):
        texte = texte_par_id.get(article["article_id"], article["title"])
        reponse, passages = generer_justification_rag(texte, article["mistral_label"], article["entreprise_cible"])

        resultats.append({
            "article_id": article["article_id"],
            "title": article["title"],
            "source_name": article["source_name"],
            "entreprise_cible": article["entreprise_cible"],
            "mistral_label": article["mistral_label"],
            "mistral_justification_rag": reponse.replace("Justification:", "").strip(),
            "evidence_used": [p["chunk_text"] for p in passages],
            "text": texte
        })

        print(f"  [{i + 1}/{len(data)}] {article['entreprise_cible']}")

        if (i + 1) % 20 == 0:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(resultats, f, ensure_ascii=False, indent=2)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(resultats, f, ensure_ascii=False, indent=2)

    print(f"\nTerminé ! Sauvegardé dans {output_path}")
    return resultats

if __name__ == "__main__":
    run()