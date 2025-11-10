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

/* CARD PRINCIPAL DE RESULTADO */
.full-job-card {
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    margin-bottom: 30px;
    overflow: hidden;
    border: 1px solid #eee;
}

/* CABEÇALHO DO CARD (Título, Score e GG) */
.fjc-header {
    padding: 20px 25px;
    background: #f8f9fa;
    border-bottom: 1px solid #eee;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.fjc-title {
    font-size: 22px;
    font-weight: 800;
    color: #2c3e50;
    margin: 0;
}
.fjc-gg {
    color: #1E56E0;
    font-weight: 700;
    font-size: 1.1rem;
}
.fjc-score-badge {
    font-size: 16px;
    font-weight: 800;
    padding: 6px 15px;
    border-radius: 20px;
    color: white;
}

/* METADADOS (Família, Subfamília, etc) */
.fjc-metadata {
    padding: 15px 25px;
    background: #fff;
    border-bottom: 1px solid #eee;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    font-size: 0.9rem;
    color: #555;
}
.meta-item b { color: #333; }

/* SEÇÕES DE CONTEÚDO (Role Description, etc) */
.fjc-body {
    padding: 25px;
    display: flex;
    flex-direction: column;
    gap: 20px;
}
.info-section {
    background: #fbfcfd;
    border-left: 5px solid #1E56E0; /* Cor padrão, será sobrescrita inline se necessário */
    padding: 15px 20px;
    border-radius: 0 8px 8px 0;
}
.section-title {
    font-weight: 700;
    color: #1E56E0;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 1rem;
}
.section-content {
    color: #444;
    line-height: 1.6;
    font-size: 0.95rem;
    white-space: pre-line; /* Respeita quebras de linha do Excel */
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
    df_levels = data.get("level_structure", pd.DataFrame()).fillna("")

    # Normaliza colunas
    if not df_jobs.empty: df_jobs.columns = df_jobs.columns.str.strip()
    if not df_levels.empty: df_levels.columns = df_levels.columns.str.strip()

    # Garante que todas as colunas possíveis existam para não quebrar o layout completo
    possible_cols = [
        "Job Family", "Sub Job Family", "Job Profile", "Role Description", 
        "Grade Differentiator", "Qualifications", "Global Grade", "Career Path",
        "Sub Job Family Description", "Job Profile Description", "Career Band Description",
        "Function", "Discipline", "Full Job Code", "KPIs / Specific Parameters"
    ]
    for c in possible_cols:
        if c not in df_jobs.columns: df_jobs[c] = "-"
    
    df_jobs["Global Grade"] = df_jobs["Global Grade"].astype(str).str.replace(r"\.0$", "", regex=True).str.strip()
    
    # Texto rico para o modelo (focado nas descrições principais)
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
    placeholder="Cole aqui a descrição detalhada da posição..."
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
        # Cores do score
        score_bg = "#28a745" if score > 85 else "#1E56E0" if score > 75 else "#fd7e14" if score > 60 else "#dc3545"
        
        # Renderização HTML Completa (Estilo idêntico ao solicitado)
        st.markdown(f"""
        <div class="full-job-card">
            <div class="fjc-header">
                <div>
                    <div class="fjc-title">{row['Job Profile']}</div>
                    <div class="fjc-gg">Global Grade {row['Global Grade']}</div>
                </div>
                <div class="fjc-score-badge" style="background-color: {score_bg};">
                    {score:.1f}% Match
                </div>
            </div>

            <div class="fjc-metadata">
                <div class="meta-item"><b>Família:</b> {row.get('Job Family', '-')}</div>
                <div class="meta-item"><b>Subfamília:</b> {row.get('Sub Job Family', '-')}</div>
                <div class="meta-item"><b>Carreira:</b> {row.get('Career Path', '-')}</div>
                <div class="meta-item"><b>Função:</b> {row.get('Function', '-')}</div>
                <div class="meta-item"><b>Disciplina:</b> {row.get('Discipline', '-')}</div>
                <div class="meta-item"><b>Código:</b> {row.get('Full Job Code', '-')}</div>
            </div>

            <div class="fjc-body">
                <div class="info-section" style="border-left-color: #95a5a6;">
                    <div class="section-title" style="color: #7f8c8d;">🧭 Sub Job Family Description</div>
                    <div class="section-content">{row.get('Sub Job Family Description', 'N/A')}</div>
                </div>

                <div class="info-section" style="border-left-color: #e91e63;">
                    <div class="section-title" style="color: #c2185b;">🧠 Job Profile Description</div>
                    <div class="section-content">{row.get('Job Profile Description', row['Role Description'])}</div>
                </div>

                 <div class="info-section" style="border-left-color: #673ab7;">
                    <div class="section-title" style="color: #512da8;">🏛️ Career Band Description</div>
                    <div class="section-content">{row.get('Career Band Description', 'N/A')}</div>
                </div>

                <div class="info-section" style="border-left-color: #1E56E0;">
                    <div class="section-title">🎯 Role Description (Responsabilidades Chave)</div>
                    <div class="section-content">{row['Role Description']}</div>
                </div>

                <div class="info-section" style="border-left-color: #ff9800;">
                    <div class="section-title" style="color: #e65100;">🏅 Grade Differentiator</div>
                    <div class="section-content">{row['Grade Differentiator']}</div>
                </div>
                
                {'<div class="info-section" style="border-left-color: #009688;"><div class="section-title" style="color: #00796b;">🎓 Qualifications</div><div class="section-content">' + row['Qualifications'] + '</div></div>' if row.get('Qualifications') and row['Qualifications'] != '-' else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)

    if top_results.iloc[0]["similarity"] < 0.6:
        st.info("💡 **Dica:** A aderência foi moderada. Tente detalhar mais a senioridade e o escopo de gestão na sua descrição.")
