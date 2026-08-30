import streamlit as st
from pathlib import Path

# Import des composants graphiques
from components import (
    sidebar_content, 
    companies_carousel, 
    kpi_cards, 
    sentiment_benchmark_table,
    sentiment_distribution_chart, 
    rag_benchmark_table
)

# Import des fonctions de chargement dynamique depuis votre data_loader
from data_loader import (
    load_canonical_articles_count,
    get_best_sentiment_model,
    get_best_rag_model,
    get_sentiment_benchmark_table,
    get_native_sentiment_distribution, 
    get_rag_benchmark_table
)


st.set_page_config(
    page_title="Finance AI Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Charger le CSS global
css_path = Path(__file__).resolve().parent / "style.css"
with open(css_path, "r", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# Pipeline de chargement avec cache pour éviter les lenteurs
@st.cache_data
def load_dashboard_data():
    articles_count = load_canonical_articles_count()
    best_sent_name, best_sent_acc = get_best_sentiment_model()
    best_rag_name, best_rag_score = get_best_rag_model()
    
    return articles_count, best_sent_name, best_sent_acc, best_rag_name, best_rag_score

# Récupération des vrais chiffres
count, best_model, accuracy, rag_name, rag_score = load_dashboard_data()


# Rendu de la Sidebar
with st.sidebar:
    sidebar_content()


# ==========================================
# CONTENU PRINCIPAL
# ==========================================

# 1. En-tête (Titre & Sous-titre)
st.markdown(
    """
    <div class="dashboard-header">
        <h1 class="dashboard-title">
            <span class="brand-gradient">Keyrus</span> <span class="brand-ai">AI</span> Intelligence Dashboard
        </h1>
        <p class="dashboard-subtitle">
            Financial News • Sentiment Analysis • Benchmarking
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Rendu de vos cartes KPIs existantes ---
kpi_cards(count, best_model, accuracy, rag_name, rag_score)

# ==========================================
# 3. ZONE INTERMÉDIAIRE : NEWS + DISTRIBUTION + BENCHMARK
# ==========================================

# Configuration en 3 colonnes avec des proportions adaptées
col_news, col_chart, col_table = st.columns([1.2, 1, 1.2], gap="medium")

with col_news:
    # 1. Rendu temporaire ou futur bloc de cartes d'articles
    st.markdown("##### 📰 Latest Financial News")
    st.info("Flux d'actualités financières à venir...")

with col_chart:
    # 2. Chargement et rendu du graphique Donut
    sentiment_df = get_native_sentiment_distribution()
    sentiment_distribution_chart(sentiment_df)

with col_table:
    # 3. Chargement et rendu du tableau compact
    benchmark_df = get_sentiment_benchmark_table()
    sentiment_benchmark_table(benchmark_df)

st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

# ==========================================
# 4. ZONE INFÉRIEURE : PERFORMANCE OVERVIEW & JUSTIFICATION QUALITY
# ==========================================

# Création de deux colonnes pour isoler le tableau RAG sur la droite
col_graphiques_rag, col_tableau_rag = st.columns([1.2, 1.5], gap="large")



with col_tableau_rag:
    # Chargement des données RAG correctement transposées par votre data_loader
    rag_df = get_rag_benchmark_table()
    # Affichage du tableau compact sur le côté droit
    rag_benchmark_table(rag_df)

# Espace fluide avant le carrousel
st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)

# 4. Bande défilante
companies_carousel()
