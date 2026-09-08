import json
import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import PROCESSED_DIR, REPORTS_DIR, JUSTIFICATIONS_DIR, ENTITIES_DIR


def load_json(path):
    """Charge et retourne le contenu JSON du fichier indiqué."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


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


def load_mistral_news_data():
    """
    Charge et fusionne les données pour le carrousel Mistral de manière sécurisée.
    Jointure insensible aux espaces parasites sur l'article_id.
    """
    try:
        # 1. Chargement des articles canoniques
        articles_path = PROCESSED_DIR / "articles_canonical.json"
        articles_list = load_json(articles_path) if articles_path.exists() else []
        
        # 2. Chargement du fichier des prédictions Mistral
        mistral_path = JUSTIFICATIONS_DIR / "mistral_justifications.json"
        mistral_data = load_json(mistral_path) if mistral_path.exists() else []
        
        # Indexation par article_id nettoyé
        predictions_map = {str(p["article_id"]).strip(): p for p in mistral_data if "article_id" in p}
        
        # 3. Chargement sécurisé des entités de Mistral
        entities_path = Path(__file__).resolve().parent.parent / "entities" / "entities_mistral.json"
        if not entities_path.exists():
            entities_path = ENTITIES_DIR / "entities_mistral.json"
            
        entities_data = load_json(entities_path) if entities_path.exists() else []
        # Indexation par article_id nettoyé
        entities_map = {str(e["article_id"]).strip(): e for e in entities_data if "article_id" in e}

        # 4. Fusion complète des données
        combined_carousel_data = []
        
        for art in articles_list:
            art_id = art.get("article_id")
            if not art_id:
                continue
                
            clean_id = str(art_id).strip()
            pred = predictions_map.get(clean_id, {})
            ent = entities_map.get(clean_id, {})
            
            # On ne conserve l'article que s'il possède une prédiction Mistral associée
            if clean_id in predictions_map:
                combined_carousel_data.append({
                    "article_id": art_id,
                    "title": pred.get("title", art.get("title", "No Title")),
                    "text": art.get("text", art.get("summary", "No Content Available...")),
                    "source": art.get("source_name", "Financial News").upper(),
                    "entreprise_cible": art.get("entreprise_cible", ""),
                    
                    # Extraction des clés exactes de Mistral
                    "sentiment": str(pred.get("mistral_label", "Neutral")).capitalize(),
                    "justification": pred.get("mistral_justification", "Aucune justification disponible."),
                    
                    # Extraction des clés d'entités (Secteur, Événement, Risques)
                    "secteur": ent.get("secteur", ent.get("Secteur", "N/A")),
                    "evenement": ent.get("evenement", ent.get("Événement", "N/A")),
                    "risques": ent.get("risques", ent.get("Risques", "Aucun"))
                })
                
        return combined_carousel_data
    except Exception:
        return []

def get_all_entreprises():
    """Retourne la liste triée de toutes les entreprises présentes dans articles_canonical.json"""
    json_path = PROCESSED_DIR / "articles_canonical.json"
    try:
        if json_path.exists():
            with open(json_path, "r", encoding="utf-8") as f:
                articles = json.load(f)
            entreprises = sorted(set(a.get("entreprise_cible", "") for a in articles if a.get("entreprise_cible")))
            return entreprises
        return []
    except Exception:
        return []