import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import JUSTIFICATIONS_DIR, SENTIMENTS_DIR, EVALUATION_DIR
from evaluation.evaluate_justifications import run

CONFIGS = [
    {
        "name": "finbert",
        "path": JUSTIFICATIONS_DIR / "finbert_justifications.json",
        "label_key": "finbert_label",
        "justification_key": "finbert_justification",
        "need_join": False
    },
    {
        "name": "mistral",
        "path": JUSTIFICATIONS_DIR / "mistral_justifications.json",
        "label_key": "mistral_label",
        "justification_key": "mistral_justification",
        "need_join": False
    },
    {
        "name": "mistral_rag",
        "path": SENTIMENTS_DIR / "sentiment_mistral_rag.json",
        "label_key": "mistral_label",
        "justification_key": "mistral_justification",
        "need_join": False
    },
    {
        "name": "financellama",
        "path": SENTIMENTS_DIR / "sentiment_financellama.json",
        "label_key": "financellama_label",
        "justification_key": "financellama_justification",
        "need_join": False
    }
]

def run_all():
    for cfg in CONFIGS:
        if not cfg["path"].exists():
            print(f"Fichier introuvable, on saute : {cfg['path']}")
            continue

        output_path = EVALUATION_DIR / f"evaluation_{cfg['name']}.json"
        print(f"\n=== Évaluation : {cfg['name']} ===")
        run(
            justifications_path=cfg["path"],
            label_key=cfg["label_key"],
            justification_key=cfg["justification_key"],
            output_path=output_path,
            need_join=cfg["need_join"]
        )

if __name__ == "__main__":
    run_all()