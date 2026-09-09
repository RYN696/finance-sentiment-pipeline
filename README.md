# Stage Finance Sentiment

Ce projet a pour objectif de collecter, nettoyer, enrichir et analyser des actualités financières afin d’évaluer automatiquement le sentiment associé à des entreprises et de comparer plusieurs approches d’analyse de texte en finance.

Le pipeline couvre :
- la collecte d’articles depuis plusieurs sources,
- la normalisation et la fusion des données,
- l’extraction d’entités et de contexte financier,
- la classification du sentiment avec plusieurs modèles,
- la génération de justifications explicatives,
- l’évaluation comparative des performances,
- la visualisation des résultats dans un tableau de bord Streamlit.

## Objectif du projet

L’objectif principal est d’explorer comment un système peut détecter le sentiment de nouvelles financières à partir d’articles de presse, puis expliquer ce sentiment en langage naturel.

Le projet compare notamment :
- FinBERT, un modèle spécialisé en finance,
- Mistral via Ollama,
- une approche RAG (retrieval augmented generation) avec recherche vectorielle,
- des évaluations de justifications à l’aide de modèles LLM.

## Aperçu fonctionnel

Le projet s’articule autour de plusieurs étapes :
1. collecte de données depuis Alpha Vantage, Marketaux et RSS,
2. normalisation et fusion des articles,
3. déduplication et consolidation des sources,
4. création d’une base vectorielle PostgreSQL,
5. classification du sentiment,
6. génération de justifications,
7. benchmarking des modèles,
8. affichage des résultats dans un dashboard.

## Structure du dépôt

```text
stage-finance-sentiment/
├── data/
│   ├── raw/                     # articles bruts collectés
│   ├── processed/               # articles normalisés / canoniques
│   ├── sentiments/              # sorties de sentiment
│   ├── justifications/          # justifications générées
│   ├── evaluation/              # évaluations par modèle
│   ├── reports/                 # benchmarks et comparaisons
│   ├── entities/                # entités extraites
│   ├── figures/                 # graphiques et images
│   └── ...
├── notebooks/                  # notebooks d’exploration
├── src/
│   ├── config.py               # variables globales et configuration
│   ├── pipeline.py             # orchestrateur du pipeline
│   ├── data_collection/        # scripts de collecte
│   ├── preprocessing/          # normalisation et fusion des données
│   ├── extraction/             # extraction d’entités
│   ├── sentiment/              # scripts de classification et justifications
│   ├── rag/                    # base PostgreSQL, embeddings et retrieval
│   ├── evaluation/             # benchmark et évaluation des justifications
│   ├── dashboard/              # application Streamlit
│   ├── utils/                  # utilitaires partagés
│   └── __init__.py
├── archive/
├── .env                       # variables d’environnement locales (non versionné)
├── .gitignore
├── requirements.txt
├── README.md
└── ...
```

## Sources de données

Le projet exploite plusieurs sources d’actualités :
- Alpha Vantage News Sentiment API,
- Marketaux,
- flux RSS,
- données internes déjà préparées dans le dossier data/.

Les fichiers historiques présents dans data/ permettent de réutiliser les résultats sans relancer la collecte.

## Stack technique

- Python 3.10+
- pandas, numpy, scikit-learn
- transformers
- sentence-transformers
- PyTorch
- ollama
- PostgreSQL + psycopg2
- Streamlit
- python-dotenv

## Prérequis

### 1) Créer l’environnement virtuel

```bash
python -m venv venv
```

Sous Windows :

```powershell
venv\Scripts\activate
```

Sous macOS/Linux :

```bash
source venv/bin/activate
```

### 2) Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3) Installer Ollama et les modèles LLM

Ce projet repose sur Ollama pour exécuter certains modèles locaux.

```bash
ollama pull mistral
ollama pull qwen2.5:7b
ollama pull llama3.1:8b
```

Les modèles référencés dans la configuration peuvent être ajustés dans [src/config.py](src/config.py).

### 4) Configurer les variables d’environnement

Créez un fichier .env à la racine du projet avec, au minimum :

```env
ALPHAVANTAGE_KEY=votre_cle_alpha_vantage
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=finance_sentiment
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

> Le projet utilise PostgreSQL pour la banque vectorielle RAG. Le script de création de table est dans [src/rag/setup_database.py](src/rag/setup_database.py).

## Pipeline de traitement

### 1) Collecte des données

```bash
python src/data_collection/collect_alphavantage.py
python src/data_collection/collect_marketaux.py
python src/data_collection/collect_rss.py
```

Les fichiers sont enregistrés dans le dossier data/raw/.

### 2) Normalisation et nettoyage

```bash
python src/preprocessing/normalize.py
```

Cela produit un fichier canonique dans data/processed/articles_canonical.json.

### 3) Extraction d’entités

```bash
python src/extraction/extract_entities.py
```

### 4) Analyse de sentiment

Différentes méthodes sont utilisées :

```bash
python src/sentiment/run_finbert.py
python src/sentiment/run_mistral.py
```

Les résultats sont enregistrés dans data/sentiments/.

### 5) Génération de justifications

```bash
python src/sentiment/justify_finbert.py
python src/sentiment/justify_mistral_rag.py
```

### 6) Base vectorielle RAG

Avant utilisation de la partie RAG, il faut créer la table et peupler la base :

```bash
python src/rag/setup_database.py
python src/rag/populate_database.py
```

La recherche sémantique est ensuite gérée dans [src/rag/retrieval.py](src/rag/retrieval.py).

### 7) Évaluation des modèles

```bash
python src/evaluation/run_benchmark_sentiments.py
python src/evaluation/run_benchmark_justifications.py
python src/evaluation/run_evaluate_all.py
```

Les résultats sont stockés dans data/reports/ et data/evaluation/.

## Dashboard

Le projet embarque un tableau de bord Streamlit pour visualiser :
- le nombre d’articles traités,
- le meilleur modèle de sentiment,
- les benchmarks,
- la distribution des sentiments,
- les résultats RAG,
- le flux de news Mistral.

Pour le lancer :

```bash
cd src/dashboard
streamlit run app.py
```

## Résultats typiques attendus

Le projet produit des artefacts dans les dossiers suivants :
- data/raw/ : données sources brutes,
- data/processed/ : données normalisées,
- data/sentiments/ : labels de sentiment,
- data/justifications/ : explications générées,
- data/evaluation/ : scores de qualité,
- data/reports/ : benchmarks globaux.

## Bonnes pratiques

- Garder un fichier .env local et ne pas le versionner.
- Vérifier que Ollama tourne avant d’exécuter les scripts LLM.
- Vérifier les paramètres PostgreSQL avant de lancer la partie RAG.
- Ne pas relancer des imports lourds sans nécessité dans le même shell.
- Réexécuter la normalisation si les données brutes ont changé.

## Limites et axes d’amélioration

- [src/pipeline.py](src/pipeline.py) reste un point de centralisation à compléter,
- le projet repose sur des modèles locaux et des services externes (Alpha Vantage, Ollama, PostgreSQL),
- la qualité des justifications dépend fortement du prompt et du modèle choisi,
- la gestion des erreurs réseau ou des limites API peut être améliorée.

## Contexte du projet

Ce dépôt correspond à un prototype de pipeline d’intelligence artificielle appliqué à l’analyse du sentiment financier à partir d’articles de presse.

Il a pour vocation de servir de base de démonstration, de benchmark et de prototypage pour des analyses de marchés financiers assistées par IA.

## Licence

Aucune licence spécifique n’a été déclarée dans ce dépôt. Vérifiez les règles internes du projet avant toute diffusion ou exploitation commerciale.
