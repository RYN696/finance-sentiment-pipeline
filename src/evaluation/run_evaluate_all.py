import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import JUSTIFICATIONS_DIR, SENTIMENTS_DIR, EVALUATION_DIR
from evaluation.evaluate_justifications import run

CONFIGS = [
    {
        "name": "financellama_rag",
        "path": JUSTIFICATIONS_DIR / "financellama_justifications_rag.json",
        "label_key": "financellama_label",
        "justification_key": "financellama_justification_rag",
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
            need_join=cfg["need_join"],
            max_articles=100
        )

if __name__ == "__main__":
    run_all()