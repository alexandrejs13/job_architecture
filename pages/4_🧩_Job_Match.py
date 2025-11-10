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
# ESTILO (ADAPTADO PARA CARDS LADO A LADO)
# ===========================================================
st.markdown("""
<style>
/* Permite que o container ocupe mais espaço para caber 3 cards lado a lado */
.block-container {
    max-width: 95% !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
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
    height: 100%; /* Para que todos os cards na mesma linha tenham a mesma altura se usar flex */
    display: flex;
    flex-direction: column;
}

/* CABEÇALHO DO CARD */
.fjc-header {
    padding: 15px 20px;
    background: #f8f9fa;
    border-bottom: 1px solid #eee;
}
.fjc-title {
    font-size: 18px;
    font-weight: 800;
    color: #2c3e50;
    margin: 0 0 5px 0;
    line-height: 1.3;
    min-height: 48px; /* Altura mínima para alinhar títulos de tamanhos diferentes */
    display: flex;
    align-items: center;
}
.fjc-gg-score {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 10px;
}
.fjc-gg {
    color: #1E56E0;
    font-weight: 700;
    font-size: 1rem;
}
.fjc-score-badge {
    font-size: 14px;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 15px;
    color: white;
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
    gap: 5px;
}
.meta-row {
    display: flex;
    justify-content: space-between;
}
.meta-item strong { color: #333; font-weight: 700; }

/* CORPO DO CARD */
.fjc-body {
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 15px;
    flex-grow: 1; /* Faz o corpo ocupar o espaço restante */
    font-size: 0.9rem;
}

/* SEÇÕES COLORIDAS */
.info-section {
    background: #fff;
    border-left-width: 4px;
    border-left-style: solid;
    padding: 0 0 0 15px;
}
.section-title {
    font-weight: 700;
    font-size: 0.95rem;
    margin-bottom: 5px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.section-content {
    color: #444;
    line-height: 1.5;
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

    # Limpeza do Global Grade
    df_jobs["Global Grade"] = df_jobs["Global Grade"].astype(str).str.replace(r"\.0$", "", regex=True).str.strip()
    
    # Texto rico para o modelo (focado no essencial para matching)
    df_jobs["Rich_Text"] = (
        df_jobs["Job Profile"] + ". " +
        df_jobs["Role Description"] + ". " +
        df_jobs["Grade Differentiator"] + ". " +
        df_jobs["Qualifications"]
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
    "📋 Cole aqui a descrição detalhada da posição (Mínimo 50 palavras):",
    height=150,
    placeholder="Descreva as principais responsabilidades, escopo de atuação, nível de autonomia, gestão de pessoas e requisitos técnicos..."
)

word_count = len(desc_input.strip().split())
st.caption(f"Contagem de palavras: {word_count} / 50")

if st.button("🔍 Analisar Aderência", type="primary", use_container_width=True):
    # --- Validação ---
    errors = []
    if selected_family == "Selecione...": errors.append("• Selecionar a **Família**.")
    if selected_subfamily == "Selecione...": errors.append("• Selecionar a **Subfamília**.")
    if word_count < 50: errors.append(f"• Detalhar mais a descrição (faltam {50 - word_count} palavras).")
    
    if errors:
        st.warning("⚠️ Para uma análise precisa, por favor:\n" + "\n".join(errors))
        st.stop()

    # --- Filtragem e Matching ---
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
    # RENDERIZAÇÃO LADO A LADO (USANDO COLUNAS)
    # ===========================================================
    st.markdown("---")
    st.subheader("🏆 Cargos Mais Compatíveis")

    # Cria 3 colunas iguais para os resultados
    cols = st.columns(3)

    for i, (idx, row) in enumerate(top_results.iterrows()):
        score = row["similarity"] * 100
        score_bg = "#28a745" if score > 85 else "#1E56E0" if score > 75 else "#fd7e14" if score > 60 else "#dc3545"
        
        # Usa a coluna correspondente para renderizar o card
        with cols[i]:
            st.markdown(f"""
            <div class="full-job-card">
                <div class="fjc-header">
                    <div class="fjc-title">{row['Job Profile']}</div>
                    <div class="fjc-gg-score">
                        <div class="fjc-gg">GG {row['Global Grade']}</div>
                        <div class="fjc-score-badge" style="background-color: {score_bg};">
                            {score:.1f}% Match
                        </div>
                    </div>
                </div>

                <div class="fjc-metadata">
                    <div class="meta-row">
                        <div><strong>Família:</strong> {row.get('Job Family', '-')}</div>
                    </div>
                    <div class="meta-row">
                        <div><strong>Subfamília:</strong> {row.get('Sub Job Family', '-')}</div>
                    </div>
                     <div class="meta-row">
                        <div><strong>Carreira:</strong> {row.get('Career Path', '-')}</div>
                        <div><strong>Código:</strong> {row.get('Full Job Code', '-')}</div>
                    </div>
                </div>

                <div class="fjc-body">
                    <div class="info-section" style="border-left-color: #1E56E0;">
                        <div class="section-title" style="color: #0d47a1;">🎯 Role Description</div>
                        <div class="section-content">{row['Role Description']}</div>
                    </div>

                    <div class="info-section" style="border-left-color: #673ab7;">
                        <div class="section-title" style="color: #512da8;">🏛️ Career Band Description</div>
                        <div class="section-content">{row['Career Band Description']}</div>
                    </div>

                    <div class="info-section" style="border-left-color: #ff9800;">
                        <div class="section-title" style="color: #e65100;">🏅 Grade Differentiator</div>
                        <div class="section-content">{row['Grade Differentiator']}</div>
                    </div>
                    
                    {f'''<div class="info-section" style="border-left-color: #009688;">
                        <div class="section-title" style="color: #00796b;">🎓 Qualifications</div>
                        <div class="section-content">{row['Qualifications']}</div>
                    </div>''' if row['Qualifications'] and str(row['Qualifications']).strip() not in ['-', '', 'nan'] else ''}

                </div> </div> """, unsafe_allow_html=True)

    if top_results.iloc[0]["similarity"] < 0.6:
        st.info("💡 **Dica:** Aderência moderada. Tente refinar a descrição com termos mais específicos.")
