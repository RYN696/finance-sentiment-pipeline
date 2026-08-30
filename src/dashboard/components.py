import streamlit as st
from pathlib import Path
import base64

def get_base64_image(image_path):
    """Convertit une image locale en chaîne Base64 propre (sans retours à la ligne)"""
    if Path(image_path).exists():
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode().replace("\n", "").strip()
    return ""

def sidebar_content():
    logo_path = Path(__file__).resolve().parent / "logos" / "keyrus_ai.png"
    st.image(str(logo_path), use_container_width=True)
    st.markdown('<div class="nav-item-active">Overview</div>', unsafe_allow_html=True)

def companies_carousel():
    """Génère la bande défilante de logos via la fonction native st.html"""
    logos_dir = Path(__file__).resolve().parent / "logos"
    
    nv = get_base64_image(logos_dir / "nvidia.png")
    ts = get_base64_image(logos_dir / "tesla.png")
    ap = get_base64_image(logos_dir / "apple.png")
    ms = get_base64_image(logos_dir / "microsoft.png")
    tte = get_base64_image(logos_dir / "TTE.png")
    jpm = get_base64_image(logos_dir / "JPM.png")
    jj = get_base64_image(logos_dir / "JJ.png")
    meta = get_base64_image(logos_dir / "meta.png")
    goo = get_base64_image(logos_dir / "google.png")
    wlt = get_base64_image(logos_dir / "wl.png")
    ntflx = get_base64_image(logos_dir / "netflix.png")
    ds = get_base64_image(logos_dir / "disney.png")
    bnp = get_base64_image(logos_dir / "bnp.png")

    html_content = (
        '<div class="carousel-container">'
        '<p class="carousel-title">Companies Tracked</p>'
        '<div class="slider">'
        '<div class="slide-track">'
        f'<div class="slide"><img src="data:image/png;base64,{nv}" alt="Nvidia"></div>'
        f'<div class="slide"><img src="data:image/png;base64,{ts}" alt="Tesla"></div>'
        f'<div class="slide"><img src="data:image/png;base64,{ap}" alt="Apple"></div>'
        f'<div class="slide"><img src="data:image/png;base64,{ms}" alt="Microsoft"></div>'
        f'<div class="slide"><img src="data:image/png;base64,{tte}" alt="TTE"></div>'
        f'<div class="slide"><img src="data:image/png;base64,{jpm}" alt="JPM"></div>'
        f'<div class="slide"><img src="data:image/png;base64,{jj}" alt="JJ"></div>'
        f'<div class="slide"><img src="data:image/png;base64,{meta}" alt="Meta"></div>'
        f'<div class="slide"><img src="data:image/png;base64,{goo}" alt="Google"></div>'
        f'<div class="slide"><img src="data:image/png;base64,{wlt}" alt="Walmart"></div>'
        f'<div class="slide"><img src="data:image/png;base64,{ntflx}" alt="Netflix"></div>'
        f'<div class="slide"><img src="data:image/png;base64,{ds}" alt="Disney"></div>'
        f'<div class="slide"><img src="data:image/png;base64,{bnp}" alt="BNP"></div>'
        f'<div class="slide"><img src="data:image/png;base64,{nv}" alt="Nvidia"></div>'
        f'<div class="slide"><img src="data:image/png;base64,{ts}" alt="Tesla"></div>'
        f'<div class="slide"><img src="data:image/png;base64,{ap}" alt="Apple"></div>'
        f'<div class="slide"><img src="data:image/png;base64,{ms}" alt="Microsoft"></div>'
        f'<div class="slide"><img src="data:image/png;base64,{tte}" alt="TTE"></div>'
        f'<div class="slide"><img src="data:image/png;base64,{jpm}" alt="JPM"></div>'
        f'<div class="slide"><img src="data:image/png;base64,{jj}" alt="JJ"></div>'
        f'<div class="slide"><img src="data:image/png;base64,{meta}" alt="Meta"></div>'
        f'<div class="slide"><img src="data:image/png;base64,{goo}" alt="Google"></div>'
        f'<div class="slide"><img src="data:image/png;base64,{wlt}" alt="Walmart"></div>'
        f'<div class="slide"><img src="data:image/png;base64,{ntflx}" alt="Netflix"></div>'
        f'<div class="slide"><img src="data:image/png;base64,{ds}" alt="Disney"></div>'
        f'<div class="slide"><img src="data:image/png;base64,{bnp}" alt="BNP"></div>'
        '</div>'
        '</div>'
        '</div>'
    )
    st.html(html_content)

def kpi_cards(count, best_model, accuracy_val, rag_name, rag_score):
    """Affiche les 3 premières cartes KPIs connectées dynamiquement"""
    
    # Formatage propre du pourcentage (ex: 0.618 -> 61.8%)
    acc_formatted = f"{accuracy_val * 100:.1f}%" if accuracy_val <= 1.0 else f"{accuracy_val:.1f}%"
        
    html_kpis = (
        '<!-- Import des icônes Google -->'
        '<div class="kpi-row">'
            '<!-- Carte 1: Total Articles -->'
            '<div class="kpi-card">'
                '<div class="kpi-content">'
                    '<p class="kpi-title">Total Articles</p>'
                    f'<h3 class="kpi-value">{count}</h3>'
                    '<p class="kpi-subtitle">With native sentiment</p>'
                '</div>'
            '</div>'

            '<!-- Carte 2: Best Model (Sentiment) -->'
            '<div class="kpi-card">'
                '<div class="kpi-content">'
                    '<p class="kpi-title">Best Model (Sentiment)</p>'
                    f'<h3 class="kpi-value model-name">{best_model}</h3>'
                    f'<p class="kpi-subtitle">Accuracy: <span class="bold-sub">{acc_formatted}</span></p>'
                '</div>'
            '</div>'

            '<!-- Carte 3: Best Global Score (RAG) -->'
            '<div class="kpi-card">'
                '<div class="kpi-content">'
                    '<p class="kpi-title">Best Global Score (RAG)</p>'
                    f'<h3 class="kpi-value">{rag_score:.2f} <span class="value-max">/ 5</span></h3>'
                    f'<p class="kpi-subtitle">{rag_name}</p>'
                '</div>'
            '</div>'
        '</div>'
    )
    st.html(html_kpis)

def sentiment_benchmark_table(df):
    """Génère le tableau de classification au format HTML statique avec le même style que le tableau RAG"""
    st.markdown("<h6 style='margin:0 0 4px 0; font-size:13px; font-weight:600;'>Sentiment Model Comparison</h6>", unsafe_allow_html=True)
    
    if df.empty:
        st.info("Aucune donnée disponible pour le tableau de benchmark.")
        return

    # Normalisation forcée des colonnes en minuscules pour la cohérence des calculs
    df.columns = df.columns.str.lower()
    
    # Correction automatique de l'échelle si données décimales
    if "accuracy" in df.columns and df["accuracy"].max() <= 1.0:
        df["accuracy"] = df["accuracy"] * 100
    if "macro_f1" in df.columns and df["macro_f1"].max() <= 1.0:
        df["macro_f1"] = df["macro_f1"] * 100

    # Sélection des colonnes dans le bon ordre et renommage des en-têtes
    df_display = df[["methode", "accuracy", "macro_f1", "cohen_kappa", "mcc"]].copy()
    df_display.columns = ["Model", "Accuracy", "Macro-F1", "Cohen-Kappa", "MCC"]

    # Formatage des valeurs textuelles pour l'affichage propre
    df_display["Accuracy"] = df_display["Accuracy"].apply(lambda x: f"{x:.1f}%")
    df_display["Macro-F1"] = df_display["Macro-F1"].apply(lambda x: f"{x:.1f}%")
    df_display["Cohen-Kappa"] = df_display["Cohen-Kappa"].apply(lambda x: f"{x:.3f}")
    df_display["MCC"] = df_display["MCC"].apply(lambda x: f"{x:.3f}")
    # Définir la colonne "Model" comme index principal pour supprimer les numéros de ligne
    df_display = df_display.set_index("Model")
    # Utilisation de st.table pour hériter du même style sans barres de défilement
    st.table(df_display)


def rag_benchmark_table(df):
    """Affiche le tableau RAG complet, entièrement visible sans scroll et avec les vrais noms de modèles"""
    st.markdown("<h6 style='margin:0 0 4px 0; font-size:13px; font-weight:600;'>🔮 Justification Quality Benchmark (RAG vs No-RAG)</h6>", unsafe_allow_html=True)
    
    if df.empty:
        st.info("Aucune donnée disponible.")
        return
        
    # Définition de l'ordre exact des colonnes avec les vrais noms complets
    cols = ["Metric", "Llama3.1", "Mistral", "Finance-Llama", "Llama3.1-RAG", "Mistral-RAG", "Finance-Llama-RAG"]
    
    # On filtre le DataFrame pour ne garder que les colonnes voulues dans le bon ordre
    df_display = df[cols].copy()
    
    # Formatage des valeurs numériques à 2 décimales pour toutes les colonnes de modèles
    for col in cols[1:]:
        df_display[col] = df_display[col].apply(lambda x: f"{x:.2f}")
        
    # L'utilisation de st.table garantit qu'aucune ligne ni colonne n'est cachée ou tronquée
    st.table(df_display)







import plotly.express as px

def sentiment_distribution_chart(df):
    """Génère un Donut Chart Plotly compact aux couleurs officielles du logo Keyrus"""
    st.markdown("##### Native Sentiment Distribution")
    
    if df.empty:
        st.info("Aucune donnée de sentiment disponible.")
        return

    # COULEURS DU LOGO KEYRUS : Bleu nuit, Bleu vif, Orange
    # On les associe astucieusement à vos 3 classes de sentiment
    color_map = {
        "Positive": "#53D4FF",  # Bleu Nuit (Couleur principale Keyrus)
        "Neutral": "#e78300",   # Bleu Vif (Couleur secondaire Keyrus)
        "Negative": "#c34517"   # Orange (Point d'accent Keyrus)
    }

    fig = px.pie(
        df, 
        values="Count", 
        names="Sentiment", 
        hole=0.65,  # Anneau légèrement plus fin pour un effet moderne
        color="Sentiment",
        color_discrete_map=color_map
    )

    fig.update_traces(
        textinfo="percent+label", 
        textposition="outside",
        hovertemplate="<b>%{label}</b><br>Articles: %{value}<br>Proportion: %{percent}<extra></extra>"
    )
    
    fig.update_layout(
        showlegend=False,
        # Réduction maximale des marges pour épouser la colonne étroite
        margin=dict(t=0, b=0, l=0, r=0), 
        height=160, # Hauteur compacte optimale
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )


    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})






