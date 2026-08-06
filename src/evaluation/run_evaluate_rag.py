import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import RESULTATS_MISTRAL_RAG, EVALUATION_DIR
from evaluation.evaluate_justifications import run

def run_evaluation_rag():
    output_path = EVALUATION_DIR / "evaluation_justifications_rag.json"
    return run(
        justifications_path=RESULTATS_MISTRAL_RAG,
        label_key="mistral_label",
        justification_key="mistral_justification",
        output_path=output_path
    )

if __name__ == "__main__":
    run_evaluation_rag()