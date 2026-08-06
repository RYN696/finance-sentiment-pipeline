import json
import sys
from pathlib import Path
import numpy as np
import ollama
from sentence_transformers import SentenceTransformer

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import RAG_BANQUE, RAG_TEST_SET, RESULTATS_MISTRAL_RAG, SENTIMENTS_DIR, MODEL_MISTRAL, MODEL_EMBEDDINGS
from utils.text_parsing import extraire_label, extraire_justification

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def trouver_exemples_similaires(embedding_article, banque, embeddings_banque, k=4):
    similarites = [cosine_similarity(embedding_article, emb) for emb in embeddings_banque]
    indices_tries = np.argsort(similarites)[::-1][:k]
    return [banque[i] for i in indices_tries]

def construire_prompt(texte, exemples):
    bloc_exemples = ""
    for ex in exemples:
        bloc_exemples += f'Article: "{ex["title"]} {ex["summary"]}"\nSentiment: {ex["api_label_normalise"]}\n\n'

    return f"""You are a financial analyst classifying the sentiment of a news article for investors, following the same classification logic as a professional financial data provider.

Here are similar real examples with their correct sentiment classification:

{bloc_exemples}
Now classify the following article using the SAME logic and level of strictness as shown in the examples above.

Respond in this exact format:
Sentiment: [positive/negative/neutral]
Justification: [1-2 sentences explaining why]

Article: {texte}"""

def run(output_path=None):
    with open(RAG_BANQUE, "r", encoding="utf-8") as f:
        banque = json.load(f)
    with open(RAG_TEST_SET, "r", encoding="utf-8") as f:
        test_set = json.load(f)

    print(f"Banque : {len(banque)} | Test set : {len(test_set)}")
    print("Chargement du modèle d'embeddings...")
    embed_model = SentenceTransformer(MODEL_EMBEDDINGS)
    embeddings_banque = np.array([a["embedding"] for a in banque])

    resultats = []
    output_path = output_path or RESULTATS_MISTRAL_RAG
    SENTIMENTS_DIR.mkdir(parents=True, exist_ok=True)

    for i, article in enumerate(test_set):
        texte = f"{article['title']} {article['summary']}"
        embedding_article = embed_model.encode([texte])[0]
        exemples = trouver_exemples_similaires(embedding_article, banque, embeddings_banque)

        prompt = construire_prompt(texte, exemples)
        reponse = ollama.generate(model=MODEL_MISTRAL, prompt=prompt)["response"]

        resultats.append({
            "entreprise_cible": article["entreprise_cible"],
            "title": article["title"],
            "summary": article["summary"],
            "api_label_normalise": article["api_label_normalise"],
            "mistral_reponse": reponse,
            "mistral_label": extraire_label(reponse),
            "mistral_justification": extraire_justification(reponse)
        })

        print(f"  [{i + 1}/{len(test_set)}] {article['entreprise_cible']} -> {resultats[-1]['mistral_label']} (API: {article['api_label_normalise']})")

        if (i + 1) % 20 == 0:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(resultats, f, ensure_ascii=False, indent=2)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(resultats, f, ensure_ascii=False, indent=2)

    print(f"\nTerminé ! {len(resultats)} résultats sauvegardés dans {output_path}")
    return resultats

if __name__ == "__main__":
    run()