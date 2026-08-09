import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import SENTIMENTS_DIR, EVALUATION_DIR
from evaluation.evaluate_justifications import run

def run_evaluation_marketaux():
    justifications_path = SENTIMENTS_DIR / "sentiment_mistral_marketaux.json"
    output_path = EVALUATION_DIR / "evaluation_justifications_marketaux.json"

    return run(
        justifications_path=justifications_path,
        label_key="mistral_label",
        justification_key="mistral_justification",
        output_path=output_path
    )

if __name__ == "__main__":
    run_evaluation_marketaux()