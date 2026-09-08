import streamlit as st
from pathlib import Path

from components import (
    sidebar_content, 
    companies_carousel, 
    kpi_cards, 
    sentiment_benchmark_table,
    sentiment_distribution_chart, 
    rag_benchmark_table,
    latest_financial_news_carousel
)

from data_loader import (
    load_canonical_articles_count,
    get_best_sentiment_model,
    get_best_rag_model,
    get_sentiment_benchmark_table,
    get_native_sentiment_distribution, 
    get_rag_benchmark_table,
    load_mistral_news_data
)

st.set_page_config(page_title="Finance AI Dashboard", layout="wide", initial_sidebar_state="expanded")

css_path = Path(__file__).resolve().parent / "style.css"
with open(css_path, "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

@st.cache_data
def load_dashboard_data():
    articles_count = load_canonical_articles_count()
    best_sent_name, best_sent_acc = get_best_sentiment_model()
    best_rag_name, best_rag_score = get_best_rag_model()
    return articles_count, best_sent_name, best_sent_acc, best_rag_name, best_rag_score

count, best_model, accuracy, rag_name, rag_score = load_dashboard_data()

with st.sidebar:
    sidebar_content()

st.markdown(
    """
    <div class="dashboard-header">
        <h1 class="dashboard-title">
            <span class="brand-gradient">Keyrus</span> <span class="brand-ai">AI</span> Intelligence Dashboard
        </h1>
        <p class="dashboard-subtitle">Financial News • Sentiment Analysis • Benchmarking</p>
    </div>
    """,
    unsafe_allow_html=True
)

kpi_cards(count, best_model, accuracy, rag_name, rag_score)

# ==========================================
# ZONE PRINCIPALE : GAUCHE (News pleine hauteur) / DROITE (empilé)
# ==========================================
col_news, col_right = st.columns([1, 1.6], gap="large")

with col_news:
    mistral_news = load_mistral_news_data()
    latest_financial_news_carousel(mistral_news)

with col_right:
    sub_chart, sub_table = st.columns([1, 1.2], gap="medium")
    with sub_chart:
        sentiment_df = get_native_sentiment_distribution()
        sentiment_distribution_chart(sentiment_df)
    with sub_table:
        benchmark_df = get_sentiment_benchmark_table()
        sentiment_benchmark_table(benchmark_df)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    rag_df = get_rag_benchmark_table()
    rag_benchmark_table(rag_df)

st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
companies_carousel()