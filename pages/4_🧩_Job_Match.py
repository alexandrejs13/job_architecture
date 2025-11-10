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
# ESTILO (CSS REFORÇADO PARA CARDS COMPLETOS)
# ===========================================================
st.markdown("""
<style>
.block-container {max-width: 1200px !important;}
.stTextArea textarea {font-size: 16px !important;}

/* CARD PRINCIPAL */
.full-job-card {
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    margin-bottom: 40px;
    border: 1px solid #e0e0e0;
    overflow: hidden;
}

/* CABEÇALHO DO CARD */
.fjc-header {
    padding: 20px 30px;
    background: #f8f9fa;
    border-bottom: 1px solid #eee;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}
.fjc-title-block {
    flex: 1;
}
.fjc-title {
    font-size: 24px;
    font-weight: 800;
    color: #2c3e50;
    margin: 0 0 5px 0;
    line-height: 1.2;
}
.fjc-gg {
    color: #1E56E0;
    font-weight: 700;
    font-size: 1.1rem;
}
.fjc-score-badge {
    font-size: 18px;
    font-weight: 800;
    padding: 8px 18px;
    border-radius: 30px;
    color: white;
    white-space: nowrap;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

/* METADADOS */
.fjc-metadata {
    padding: 15px 30px;
    background: #fff;
    border-bottom: 1px solid #eee;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 12px;
    font-size: 0.9rem;
    color: #555;
}
.meta-item strong { color: #333; font-weight: 700; }

/* CORPO DO CARD */
.fjc-body {
    padding: 30px;
    display: flex;
    flex-direction: column;
    gap: 25px;
}

/* SEÇÕES COLORIDAS */
.info-section {
    background: #fff;
    border-left-width: 5px;
    border-left-style: solid;
    padding: 0 0 0 20px;
}
.section-title {
    font-weight: 700;
    font-size: 1.05rem;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-content {
    color: #444;
    line-height: 1.6;
    font-size: 0.95rem;
    white-space: pre-wrap;
}
</style>
""", unsafe_allow_html=True)

# ===========================================================
# CARREGAMENTO DE DADOS E MODELO
# ===========================================================
@st.cache_resource
def load_model():
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

@st.cache_data(show_spinner=False)
def load_data_and_embeddings():
    data = load_excel_data()
    df_jobs = data.get("job_profile", pd.DataFrame()).fillna("")
    
    # Normaliza nomes de colunas
    if not df_jobs.empty: df_jobs.columns = df_jobs.columns.str.strip()

    # Garante existência de todas as colunas necessárias
    cols_needed = [
        "Job Family", "Sub Job Family", "Job Profile", "Role Description", 
        "Grade Differentiator", "Qualifications", "Global Grade", "Career Path",
        "Sub Job Family Description", "Job Profile Description", "Career Band Description",
        "Function", "Discipline", "Full Job Code", "KPIs / Specific Parameters"
    ]
    for c in cols_needed:
        if c not in df_jobs.columns: df_jobs[c] = "-"

    df_jobs["Global Grade"] = df_jobs["Global Grade"].astype(str).str.replace(r"\.0$", "", regex=True).str.strip()
    
    # --- CRIAÇÃO DO TEXTO RICO PARA MATCHING (REFINADO) ---
    # Foco exclusivo nos campos que diferenciam os cargos, ignorando os genéricos.
    df_jobs["Rich_Text"] = (
        "Job Profile: " + df_jobs["Job Profile"] + ". " +
        "Role Description: " + df_jobs["Role Description"] + ". " +
        "Grade Differentiator (Level Specifics): " + df_jobs["Grade Differentiator"] + ". " +
        "Career Band Context: " + df_jobs["Career Band Description"] + ". " +
        "Requirements: " + df_jobs["Qualifications"]
    )

    model = load_model()
    embeddings = model.encode(df_jobs["Rich_Text"].tolist(), show_progress_bar=True)

    return df_jobs, embeddings

try:
    df, job_embeddings = load_data_and_embeddings()
    model = load_model()
except Exception as e:
    st.error(f"Erro crítico ao carregar dados: {e}")
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
    "📋 Descreva as responsabilidades e requisitos (Mínimo 50 palavras):",
    height=200,
    placeholder="Descreva as principais responsabilidades, escopo de atuação, nível de autonomia, gestão de pessoas e requisitos técnicos..."
)

word_count = len(desc_input.strip().split())
st.caption(f"Contagem de palavras: {word_count} / 50")

if st.button("🔍 Analisar Aderência", type="primary", use_container_width=True):
    # Validação
    errors = []
    if selected_family == "Selecione...": errors.append("• Selecionar a Família.")
    if selected_subfamily == "Selecione...": errors.append("• Selecionar a Subfamília.")
    if word_count < 50: errors.append(f"• Detalhar mais a descrição (faltam {50 - word_count} palavras).")
    
    if errors:
        st.warning("⚠️ Para uma análise precisa, por favor:\n" + "\n".join(errors))
        st.stop()

    # Filtragem e Matching
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

    # ===========================================================
    # RENDERIZAÇÃO DOS CARDS COMPLETOS
    # ===========================================================
    st.markdown("---")
    st.subheader("🏆 Cargos Mais Compatíveis")

    for i, (idx, row) in enumerate(top_results.iterrows()):
        score = row["similarity"] * 100
        score_bg = "#28a745" if score > 85 else "#1E56E0" if score > 75 else "#fd7e14" if score > 60 else "#dc3545"
        
        st.markdown(f"""
        <div class="full-job-card">
            <div class="fjc-header">
                <div class="fjc-title-block">
                    <div class="fjc-title">{row['Job Profile']}</div>
                    <div class="fjc-gg">Global Grade {row['Global Grade']}</div>
                </div>
                <div class="fjc-score-badge" style="background-color: {score_bg};">
                    {score:.1f}% Match
                </div>
            </div>

            <div class="fjc-metadata">
                <div class="meta-item"><strong>Família:</strong> {row['Job Family']}</div>
                <div class="meta-item"><strong>Subfamília:</strong> {row['Sub Job Family']}</div>
                <div class="meta-item"><strong>Carreira:</strong> {row['Career Path']}</div>
                <div class="meta-item"><strong>Função:</strong> {row['Function']}</div>
                <div class="meta-item"><strong>Disciplina:</strong> {row['Discipline']}</div>
                <div class="meta-item"><strong>Código:</strong> {row['Full Job Code']}</div>
            </div>

            <div class="fjc-body">
                <div class="info-section" style="border-left-color: #95a5a6;">
                    <div class="section-title" style="color: #7f8c8d;">🧭 Sub Job Family Description</div>
                    <div class="section-content">{row['Sub Job Family Description']}</div>
                </div>
                <div class="info-section" style="border-left-color: #e91e63;">
                    <div class="section-title" style="color: #c2185b;">🧠 Job Profile Description</div>
                    <div class="section-content">{row['Job Profile Description']}</div>
                </div>
                 <div class="info-section" style="border-left-color: #673ab7;">
                    <div class="section-title" style="color: #512da8;">🏛️ Career Band Description</div>
                    <div class="section-content">{row['Career Band Description']}</div>
                </div>
                <div class="info-section" style="border-left-color: #1E56E0;">
                    <div class="section-title" style="color: #0d47a1;">🎯 Role Description</div>
                    <div class="section-content">{row['Role Description']}</div>
                </div>
                <div class="info-section" style="border-left-color: #ff9800;">
                    <div class="section-title" style="color: #e65100;">🏅 Grade Differentiator</div>
                    <div class="section-content">{row['Grade Differentiator']}</div>
                </div>
                {f'''<div class="info-section" style="border-left-color: #009688;">
                    <div class="section-title" style="color: #00796b;">🎓 Qualifications</div>
                    <div class="section-content">{row['Qualifications']}</div>
                </div>''' if row['Qualifications'] and str(row['Qualifications']).strip() not in ['-', '', 'nan'] else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)

    if top_results.iloc[0]["similarity"] < 0.6:
        st.info("💡 **Dica:** Aderência moderada. Tente refinar a descrição com termos mais específicos da sua área.")
