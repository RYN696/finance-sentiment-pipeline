import json
import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import PROCESSED_DIR, REPORTS_DIR

def load_canonical_articles_count():
    """Lit le fichier articles_canonical.json et renvoie le nombre total d'articles uniques"""
    json_path = PROCESSED_DIR / "articles_canonical.json"
    
    try:
        if json_path.exists():
            with open(json_path, "r", encoding="utf-8") as f:
                articles = json.load(f)
                if isinstance(articles, list):
                    return len(articles)
        return 0
    except Exception:
        return 0

def get_best_sentiment_model():
    """Lit benchmark_sentiments.json et retourne le meilleur modèle et son accuracy"""

    
    json_path = REPORTS_DIR / "benchmark_sentiments.json"
    
    try:
        if json_path.exists():
            # Chargement des données dans un DataFrame Pandas
            with open(json_path, "r", encoding="utf-8") as f:
                df = pd.DataFrame(json.load(f))
            
            if not df.empty and "accuracy" in df.columns:
                # Tri ou recherche de la ligne ayant la valeur maximale d'accuracy
                best_row_idx = df["accuracy"].astype(float).idxmax()
                best_model_row = df.loc[best_row_idx]
                
                # Récupération de la méthode et de la valeur brute
                model_name = best_model_row.get("methode", "N/A")
                accuracy_val = float(best_model_row["accuracy"])
                
                return model_name, accuracy_val
        return "N/A", 0.0
    except Exception:
        return "N/A", 0.0


def get_best_rag_model():
    """Lit benchmark_justifications.json et extrait le modèle ayant le meilleur SCORE GLOBAL"""
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from config import REPORTS_DIR
    
    json_path = REPORTS_DIR / "benchmark_justifications.json"
    
    try:
        if json_path.exists():
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # On cible directement le dictionnaire lié à la clé "SCORE GLOBAL"
            score_global_data = data.get("SCORE GLOBAL", {})
            
            if score_global_data:
                # max() cherche la clé (le nom du modèle) possédant la valeur numérique la plus élevée
                best_model_name = max(score_global_data, key=score_global_data.get)
                best_score = float(score_global_data[best_model_name])
                
                return best_model_name, best_score
                
        return "N/A", 0.0
    except Exception:
        return "N/A", 0.0
def get_sentiment_benchmark_table():
    """Lit benchmark_sentiments.json et retourne un DataFrame propre trié par performance"""
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from config import REPORTS_DIR
    
    json_path = REPORTS_DIR / "benchmark_sentiments.json"
    
    try:
        if json_path.exists():
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            df = pd.DataFrame(data)
            if not df.empty:
                # Optionnel : renommer ou réordonner les colonnes pour matcher la maquette
                # Colonnes attendues : methode, articles (ou n_articles), accuracy, macro_f1, kappa, mcc
                if "accuracy" in df.columns:
                    df = df.sort_values(by="accuracy", ascending=False)
                return df
        return pd.DataFrame()
    except Exception:
        return pd.DataFrame()

def get_native_sentiment_distribution():
    """Lit articles_canonical.json et compte la distribution des sentiments natifs"""
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from config import PROCESSED_DIR
    
    json_path = PROCESSED_DIR / "articles_canonical.json"
    
    try:
        if json_path.exists():
            with open(json_path, "r", encoding="utf-8") as f:
                articles = json.load(f)
            
            # Récupération de tous les sentiments normalisés
            sentiments = []
            for a in articles:
                # Utilise la même logique de conversion si pas encore fait
                label = a.get("native_sentiment_label")
                score = a.get("native_sentiment_score")
                
                if label:
                    if label in ["Bullish", "Somewhat-Bullish", "Positive"]: sentiments.append("Positive")
                    elif label in ["Bearish", "Somewhat-Bearish", "Negative"]: sentiments.append("Negative")
                    else: sentiments.append("Neutral")
                elif score is not None:
                    if float(score) > 0.15: sentiments.append("Positive")
                    elif float(score) < -0.15: sentiments.append("Negative")
                    else: sentiments.append("Neutral")
            
            # Création d'un DataFrame de comptage propre pour Plotly
            if sentiments:
                df_counts = pd.Series(sentiments).value_counts().reset_index()
                df_counts.columns = ["Sentiment", "Count"]
                return df_counts
                
        return pd.DataFrame(columns=["Sentiment", "Count"])
    except Exception:
        return pd.DataFrame(columns=["Sentiment", "Count"])



def get_rag_benchmark_table():
    """Lit benchmark_justifications.json, transpose les données et formate l'affichage"""
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from config import REPORTS_DIR
    
    json_path = REPORTS_DIR / "benchmark_justifications.json"
    
    try:
        if json_path.exists():
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # 1. Charger et transposer IMMÉDIATEMENT (.T) pour basculer les modèles en colonnes
            df = pd.DataFrame(data).T
            
            # 2. Convertir l'index (qui contient les métriques maintenant) en une colonne
            df = df.reset_index().rename(columns={"index": "Metric"})
            
            # 3. Capitaliser le nom des métriques pour un rendu esthétique impeccable
            df["Metric"] = df["Metric"].str.capitalize()
            
            # Optionnel : Remplacer les noms système par des libellés propres avec tirets
            rename_dict = {
                "Faithfulness": "Faithfulness",
                "Relevance": "Relevance",
                "Completeness": "Completeness",
                "Clarity": "Clarity",
                "Hallucination": "Hallucination",
                "Consistency": "Consistency",
                "Evidencegrounding": "Evidence Grounding",
                "Score global": "SCORE GLOBAL"
            }
            df["Metric"] = df["Metric"].map(rename_dict).fillna(df["Metric"])
            
            return df
        return pd.DataFrame()
    except Exception:
        return pd.DataFrame()


