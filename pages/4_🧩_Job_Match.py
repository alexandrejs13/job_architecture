# -*- coding: utf-8 -*-
# pages/4_🧩_Job_Match.py

import streamlit as st
import pandas as pd
import numpy as np
import html
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from utils.data_loader import load_excel_data
from utils.ui_components import section, lock_sidebar

# ===========================================================
# CONFIGURAÇÃO DE PÁGINA
# ===========================================================
st.set_page_config(layout="wide", page_title="🧩 Job Match")
lock_sidebar()

# ===========================================================
# ESTILO (CSS GRID PARA ALINHAMENTO PERFEITO)
# ===========================================================
st.markdown("""
<style>
.block-container {
    max-width: 98% !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}
.stTextArea textarea {font-size: 16px !important;}

/* Grid Container Principal */
.comparison-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr); /* 3 colunas iguais */
    gap: 20px;
    margin-top: 20px;
}

/* Estilo das Células do Grid */
.grid-cell {
    background: #fff;
    border: 1px solid #e0e0e0;
    padding: 15px;
    display: flex;
    flex-direction: column;
}

/* Cabeçalho (Título, GG, Score) */
.header-cell {
    background: #f8f9fa;
    border-radius: 12px 12px 0 0;
    border-bottom: none;
}
.fjc-title { font-size: 18px; font-weight: 800; color: #2c3e50; margin-bottom: 10px; min-height: 50px; }
.fjc-gg-row { display: flex; justify-content: space-between; align-items: center; }
.fjc-gg { color: #1E56E0; font-weight: 700; }
.fjc-score { color: white; font-weight: 700; padding: 4px 10px; border-radius: 12px; font-size: 0.9rem; }

/* Metadados */
.meta-cell {
    border-top: 1px solid #eee;
    border-bottom: 1px solid #eee;
    font-size: 0.85rem;
    color: #555;
    min-height: 120px; /* Garante altura mínima igual */
}
.meta-row { margin-bottom: 5px; }

/* Seções de Conteúdo (com cores na borda esquerda) */
.section-cell {
    border-left-width: 5px;
    border-left-style: solid;
    border-top: none; /* Remove borda superior para conectar visualmente */
    background: #fdfdfd;
}
.section-title { font-weight: 700; font-size: 0.95rem; margin-bottom: 8px; color: #333; display: flex; align-items: center; gap: 5px;}
.section-content { color: #444; font-size: 0.9rem; line-height: 1.5; white-space: pre-wrap; }

/* Rodapé para fechar a borda */
.footer-cell {
    height: 10px;
    border-top: none;
    border-radius: 0 0 12px 12px;
    background: #fff;
}

</style>
""", unsafe_allow_html=True)

# ===========================================================
# CARREGAMENTO DE DADOS
# ===========================================================
@st.cache_resource
def load_model():
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

@st.cache_data(show_spinner=False)
def load_data_and_embeddings():
    data = load_excel_data()
    df_jobs = data.get("job_profile", pd.DataFrame()).fillna("")
    df_levels = data.get("level_structure", pd.DataFrame()).fillna("")

    if not df_jobs.empty:
        df_jobs.columns = df_jobs.columns.str.strip()
        cols_needed = [
            "Job Family", "Sub Job Family", "Job Profile", "Role Description", 
            "Grade Differentiator", "Qualifications", "Global Grade", "Career Path",
            "Sub Job Family Description", "Job Profile Description", "Career Band Description",
            "Function", "Discipline", "Full Job Code", "KPIs / Specific Parameters"
        ]
        for c in cols_needed:
            if c not in df_jobs.columns: df_jobs[c] = "-"

    if not df_levels.empty:
        df_levels.columns = df_levels.columns.str.strip()

    df_jobs["Global Grade"] = df_jobs["Global Grade"].astype(str).str.replace(r"\.0$", "", regex=True).str.strip()
    if "Global Grade" in df_levels.columns:
        df_levels["Global Grade"] = df_levels["Global Grade"].astype(str).str.replace(r"\.0$", "", regex=True).str.strip()
    
    df_jobs["Rich_Text"] = (
        df_jobs["Job Profile"] + ". " +
        df_jobs["Role Description"] + ". " +
        df_jobs["Grade Differentiator"] + ". " +
        df_jobs["Qualifications"]
    )

    model = load_model()
    embeddings = model.encode(df_jobs["Rich_Text"].tolist(), show_progress_bar=True)

    return df_jobs, df_levels, embeddings

try:
    df, df_levels, job_embeddings = load_data_and_embeddings()
    model = load_model()
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

# ===========================================================
# INTERFACE
# ===========================================================
section("🧩 Job Match")
st.markdown("Encontre o cargo ideal com base na descrição completa das responsabilidades.")

c1, c2 = st.columns(2)
with c1:
    families = sorted(df["Job Family"].unique())
    selected_family = st.selectbox("📂 Família (Obrigatório)", ["Selecione..."] + families)
with c2:
    subfamilies = []
    if selected_family != "Selecione...":
        subfamilies = sorted(df[df["Job Family"] == selected_family]["Sub Job Family"].unique())
    selected_subfamily = st.selectbox("📂 Subfamília (Obrigatório)", ["Selecione..."] + subfamilies)

desc_input = st.text_area(
    "📋 Cole aqui a descrição detalhada da posição (Mínimo 50 palavras):",
    height=150
)
word_count = len(desc_input.strip().split())
st.caption(f"Contagem de palavras: {word_count} / 50")

if st.button("🔍 Analisar Aderência", type="primary", use_container_width=True):
    if selected_family == "Selecione..." or selected_subfamily == "Selecione..." or word_count < 50:
        st.warning("⚠️ Selecione Família, Subfamília e insira uma descrição com pelo menos 50 palavras.")
        st.stop()

    mask = (df["Job Family"] == selected_family) & (df["Sub Job Family"] == selected_subfamily)
    if not mask.any():
        st.error("Não foram encontrados cargos para esta combinação.")
        st.stop()

    filtered_indices = df[mask].index
    filtered_embeddings = job_embeddings[filtered_indices]
    query_emb = model.encode([desc_input])
    sims = cosine_similarity(query_emb, filtered_embeddings)[0]
    results = df.loc[filtered_indices].copy()
    results["similarity"] = sims
    top3 = results.sort_values("similarity", ascending=False).head(3)

    # ===========================================================
    # RENDERIZAÇÃO EM GRID ÚNICO (PARA ALINHAMENTO PERFEITO)
    # ===========================================================
    st.markdown("---")
    st.subheader("🏆 Cargos Mais Compatíveis")

    if len(top3) < 1:
        st.warning("Nenhum resultado encontrado.")
        st.stop()

    # Prepara os dados
    cards_data = []
    for _, row in top3.iterrows():
        score_val = row["similarity"] * 100
        score_bg = "#28a745" if score_val > 85 else "#1E56E0" if score_val > 75 else "#fd7e14" if score_val > 60 else "#dc3545"
        
        lvl_name = ""
        gg_val = str(row["Global Grade"]).strip()
        if not df_levels.empty and "Global Grade" in df_levels.columns and "Level Name" in df_levels.columns:
             match = df_levels[df_levels["Global Grade"].astype(str).str.strip() == gg_val]
             if not match.empty:
                 lvl_name = f"• {match['Level Name'].iloc[0]}"

        cards_data.append({
            "row": row,
            "score_fmt": f"{score_val:.1f}%",
            "score_bg": score_bg,
            "lvl": lvl_name
        })

    # Garante 3 slots mesmo que tenha menos resultados (para manter o grid)
    while len(cards_data) < 3:
        cards_data.append(None)

    # INÍCIO DO GRID HTML
    grid_html = '<div class="comparison-grid">'

    # --- 1. LINHA DE CABEÇALHO ---
    for card in cards_data:
        if card:
            grid_html += f"""
            <div class="grid-cell header-cell">
                <div class="fjc-title">{html.escape(card['row']['Job Profile'])}</div>
                <div class="fjc-gg-row">
                    <div class="fjc-gg">GG {card['row']['Global Grade']} {card['lvl']}</div>
                    <div class="fjc-score" style="background-color: {card['score_bg']};">{card['score_fmt']} Match</div>
                </div>
            </div>"""
        else: grid_html += "<div></div>"

    # --- 2. LINHA DE METADADOS ---
    for card in cards_data:
        if card:
            d = card['row']
            grid_html += f"""
            <div class="grid-cell meta-cell">
                <div class="meta-row"><strong>Família:</strong> {html.escape(str(d.get('Job Family','-')))}</div>
                <div class="meta-row"><strong>Subfamília:</strong> {html.escape(str(d.get('Sub Job Family','-')))}</div>
                <div class="meta-row"><strong>Carreira:</strong> {html.escape(str(d.get('Career Path','-')))}</div>
                <div class="meta-row"><strong>Cód:</strong> {html.escape(str(d.get('Full Job Code','-')))}</div>
            </div>"""
        else: grid_html += "<div></div>"

    # --- 3. SEÇÕES DE CONTEÚDO (ALINHADAS) ---
    sections = [
        ("🧭 Sub Job Family Description", "Sub Job Family Description", "#95a5a6"),
        ("🧠 Job Profile Description", "Job Profile Description", "#e91e63"),
        ("🏛️ Career Band Description", "Career Band Description", "#673ab7"),
        ("🎯 Role Description", "Role Description", "#1E56E0"),
        ("🏅 Grade Differentiator", "Grade Differentiator", "#ff9800"),
        ("🎓 Qualifications", "Qualifications", "#009688")
    ]

    for title, field, color in sections:
        for card in cards_data:
            if card:
                content = str(card['row'].get(field, '-'))
                # Só mostra Qualifications se não for vazio/nan
                if field == "Qualifications" and (len(content) < 2 or content.lower() == 'nan'):
                     grid_html += f'<div class="grid-cell section-cell" style="border-left-color: transparent; background: transparent; border: none;"></div>'
                else:
                    grid_html += f"""
                    <div class="grid-cell section-cell" style="border-left-color: {color};">
                        <div class="section-title" style="color: {color};">{title}</div>
                        <div class="section-content">{html.escape(content)}</div>
                    </div>"""
            else: grid_html += "<div></div>"

    # --- 4. RODAPÉ (FECHAMENTO) ---
    for card in cards_data:
        if card: grid_html += '<div class="grid-cell footer-cell"></div>'
        else: grid_html += "<div></div>"

    grid_html += '</div>' # Fim do Grid

    st.markdown(grid_html, unsafe_allow_html=True)

    if top3.iloc[0]["similarity"] < 0.6:
        st.info("💡 Aderência moderada. Tente refinar sua descrição.")
