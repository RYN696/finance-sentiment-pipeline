# Extraction d'information et analyse des sentiments des actualités financières

Pipeline complet de collecte, traitement et analyse de sentiment sur des actualités financières, avec comparaison de plusieurs approches (modèle spécialisé, LLM local, LLM+RAG) et évaluation automatique de la qualité des justifications générées.

## Objectif

Construire un pipeline d'extraction automatique d'information à partir d'actualités financières afin de contribuer à l'analyse des actifs boursiers, avec :
- Collecte automatique d'articles financiers
- Analyse de sentiment via plusieurs méthodes (FinBERT, Mistral, Mistral+RAG)
- Génération de justifications en langage naturel
- Évaluation de la qualité de ces justifications (LLM-as-a-Judge)
- Benchmark comparatif entre les approches

## Architecture

data/
├── raw/ # Articles bruts collectés
├── processed/ # Articles nettoyés, banque RAG
├── sentiments/ # Résultats de sentiment par méthode
├── justifications/ # Justifications générées
├── evaluation/ # Scores de qualité des justifications
└── reports/ # Comparaisons et taux d'accord

src/
├── data_collection/ # Collecte des articles (API Alpha Vantage)
├── preprocessing/ # Nettoyage, déduplication
├── sentiment/ # FinBERT, Mistral
├── rag/ # Construction de la banque RAG, classification avec RAG
├── evaluation/ # Justifications, évaluation qualité, comparaisons
├── utils/ # Fonctions partagées (parsing des réponses LLM)
├── config.py # Chemins et constantes centralisés
└── pipeline.py # Orchestrateur du pipeline complet

## Méthodes comparées

| Méthode | Description |
|---|---|
| **FinBERT** | Modèle BERT spécialisé finance, classification directe |
| **Mistral 7B** | LLM local (via Ollama), avec prompt engineering |
| **Mistral 7B + RAG** | Mistral guidé par des exemples similaires récupérés dynamiquement |
| **API Alpha Vantage** | Sentiment de référence (baseline), fourni par la source de données |

## Installation

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Créer un fichier `.env` à la racine avec :
ALPHAVANTAGE_KEY=votre_cle

Installer Ollama et télécharger les modèles utilisés :
```bash
ollama pull mistral
ollama pull qwen2.5:14b
```

## Utilisation

Lancer tout le pipeline :
```bash
python src/pipeline.py
```

Lancer une étape précise :
```bash
python src/pipeline.py --steps mistral
```

Étapes disponibles : `collect`, `prepare`, `finbert`, `mistral`, `rag_bank`, `rag_sentiment`, `justify`, `evaluate`

## Résultats (benchmark)

| Comparaison | Taux d'accord |
|---|---|
| FinBERT / Mistral | 63.7% |
| FinBERT / API | 52.4% |
| Mistral / API | 65.9% |
| Mistral + RAG / API | 67.5% |

## Technologies utilisées

Python, Transformers (FinBERT), Ollama (Mistral, Qwen 2.5), Sentence-Transformers (embeddings RAG), Pandas, Alpha Vantage API.

