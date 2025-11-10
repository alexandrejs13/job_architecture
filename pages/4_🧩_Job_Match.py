# -*- coding: utf-8 -*-
# pages/4_🧩_Job_Match.py

import streamlit as st
import pandas as pd
import numpy as np
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
# ESTILO (MANTIDO O LAYOUT APROVADO)
# ===========================================================
st.markdown("""
<style>
/* Ajuste para caber 3 cards lado a lado confortavelmente */
.block-container {
    max-width: 95% !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}
.stTextArea textarea {font-size: 16px !important;}

/* CARD PRINCIPAL */
.full-job-card {
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 20px;
    border: 1px solid #e0e0e0;
    overflow: hidden;
    height: 100%;
    display: flex;
    flex-direction: column;
}

/* CABEÇALHO */
.fjc-header {
    padding: 15px 20px;
    background: #f8f9fa;
    border-bottom: 1px solid #eee;
}
.fjc-title-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 10px;
}
.fjc-title {
    font-size: 18px;
    font-weight: 800;
    color: #2c3e50;
    line-height: 1.3;
    flex: 1;
}
.fjc-score {
    font-size: 14px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 12px;
    color: white;
    white-space: nowrap;
    margin-left: 10px;
}
.fjc-gg {
    color: #1E56E0;
    font-weight: 700;
    font-size: 0.95rem;
}

/* METADADOS */
.fjc-metadata {
    padding: 12px 20px;
    background: #fff;
    border-bottom: 1px solid #eee;
    font-size: 0.85rem;
    color: #555;
    display: flex;
    flex-direction: column;
    gap: 6px;
}
.meta-row {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
}
.meta-item strong { color: #333; font-weight: 700; }

/* CORPO */
.fjc-body {
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 20px;
    flex-grow: 1;
    background-color: #fff;
}

/* SEÇÕES COLORIDAS */
.info-section {
    background: #fdfdfd;
    border-left-width: 4px;
    border-left-style: solid;
    padding: 10px 15px;
    border-radius: 0 6px 6px 0;
    border: 1px solid #f0f0f0;
    border-left-width: 4px; /* Reforça a borda esquerda */
}
.section-title {
    font-weight: 700;
    font-size: 0.9rem;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 6px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.section-content {
    color: #444;
    line-height: 1.5;
    font-size: 0.9rem;
    white-space: pre-wrap;
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
    
    if not df_jobs.empty: df_jobs.columns = df_jobs.columns.str.strip()

    cols_needed = [
        "Job Family", "Sub Job Family", "Job Profile", "Role Description", 
        "Grade Differentiator", "Qualifications", "Global Grade", "Career Path",
        "Sub Job Family Description", "Job Profile Description", "Career Band Description",
        "Function", "Discipline", "Full Job Code", "KPIs / Specific Parameters"
    ]
    for c in cols_needed:
        if c not in df_jobs.columns: df_jobs[c] = "-"

    df_jobs["Global Grade"] = df_jobs["Global Grade"].astype(str).str.replace(r"\.0$", "", regex=True).str.strip()
    
    df_jobs["Rich_Text"] = (
        "Job Profile: " + df_jobs["Job Profile"] + ". " +
        "Role Description: " + df_jobs["Role Description"] + ". " +
        "Grade Differentiator: " + df_jobs["Grade Differentiator"] + ". " +
        "Qualifications: " + df_jobs["Qualifications"]
    )

    model = load_model()
    embeddings = model.encode(df_jobs["Rich_Text"].tolist(), show_progress_bar=True)

    return df_jobs, embeddings

try:
    df, job_embeddings = load_data_and_embeddings()
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

if st.button("🔍 Analisar Aderência", type="primary", use_container_width=True):
    if selected_family == "Selecione..." or selected_subfamily == "Selecione..." or len(desc_input.split()) < 50:
        st.warning("⚠️ Para uma análise precisa, selecione Família, Subfamília e insira uma descrição com pelo menos 50 palavras.")
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
    top_results = results.sort_values("similarity", ascending=False).head(3)

    st.markdown("---")
    st.subheader("🏆 Cargos Mais Compatíveis")

    # Layout de 3 colunas para os cards lado a lado
    cols = st.columns(3)

    for i, (idx, row) in enumerate(top_results.iterrows()):
        score = row["similarity"] * 100
        score_bg = "#28a745" if score > 85 else "#fd7e14" if score > 60 else "#dc3545"
        
        # Construção do HTML por partes para evitar erros de string
        header_html = f"""
            <div class="fjc-header">
                <div class="fjc-title-row">
                    <div class="fjc-title">{row['Job Profile']}</div>
                    <div class="fjc-score" style="background-color: {score_bg};">{score:.1f}%</div>
                </div>
                <div class="fjc-gg">Global Grade {row['Global Grade']}</div>
            </div>
        """
        
        meta_html = f"""
            <div class="fjc-metadata">
                <div class="meta-row">
                    <div class="meta-item"><strong>Família:</strong> {row.get('Job Family', '-')}</div>
                </div>
                <div class="meta-row">
                    <div class="meta-item"><strong>Subfamília:</strong> {row.get('Sub Job Family', '-')}</div>
                </div>
                 <div class="meta-row">
                    <div class="meta-item"><strong>Carreira:</strong> {row.get('Career Path', '-')}</div>
                    <div class="meta-item"><strong>Cód:</strong> {row.get('Full Job Code', '-')}</div>
                </div>
            </div>
        """

        # Seções do corpo
        s1 = f"""<div class="info-section" style="border-left-color: #95a5a6;">
                    <div class="section-title" style="color: #7f8c8d;">🧭 Sub Job Family Description</div>
                    <div class="section-content">{row.get('Sub Job Family Description', '-')}</div>
                </div>"""
        
        s2 = f"""<div class="info-section" style="border-left-color: #e91e63;">
                    <div class="section-title" style="color: #c2185b;">🧠 Job Profile Description</div>
                    <div class="section-content">{row.get('Job Profile Description', '-')}</div>
                </div>"""

        s3 = f"""<div class="info-section" style="border-left-color: #673ab7;">
                    <div class="section-title" style="color: #512da8;">🏛️ Career Band Description</div>
                    <div class="section-content">{row.get('Career Band Description', '-')}</div>
                </div>"""

        s4 = f"""<div class="info-section" style="border-left-color: #1E56E0;">
                    <div class="section-title" style="color: #0d47a1;">🎯 Role Description</div>
                    <div class="section-content">{row.get('Role Description', '-')}</div>
                </div>"""

        s5 = f"""<div class="info-section" style="border-left-color: #ff9800;">
                    <div class="section-title" style="color: #e65100;">🏅 Grade Differentiator</div>
                    <div class="section-content">{row.get('Grade Differentiator', '-')}</div>
                </div>"""
        
        s6 = ""
        if row.get('Qualifications') and str(row['Qualifications']).strip() not in ['-', '', 'nan']:
             s6 = f"""<div class="info-section" style="border-left-color: #009688;">
                        <div class="section-title" style="color: #00796b;">🎓 Qualifications</div>
                        <div class="section-content">{row['Qualifications']}</div>
                    </div>"""

        body_html = f"""<div class="fjc-body">{s1}{s2}{s3}{s4}{s5}{s6}</div>"""

        # Renderiza o card completo na coluna correta
        with cols[i]:
            st.markdown(f"""<div class="full-job-card">{header_html}{meta_html}{body_html}</div>""", unsafe_allow_html=True)
