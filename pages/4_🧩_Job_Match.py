# -*- coding: utf-8 -*-
# pages/4_🧩_Job_Match.py

import streamlit as st
import pandas as pd
import numpy as np
import html # Para escapar strings e evitar HTML bruto na tela
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
# ESTILO (CSS REFINADO PARA ALINHAMENTO FORÇADO DE SEÇÕES)
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

/* O container de cada card será um flexbox para gerenciar seus blocos internos */
.job-card-container {
    display: flex;
    flex-direction: column;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    overflow: hidden; /* Garante que bordas arredondadas funcionem */
    height: 100%; /* Importante para que as colunas se estiquem */
    margin-bottom: 20px; /* Espaçamento entre as 'linhas' de cards se houver mais de 3 */
}

/* CABEÇALHO do Card */
.card-header-block {
    background-color: #f8f9fa;
    padding: 20px;
    border-bottom: 1px solid #eee;
    min-height: 120px; /* Garante altura mínima para cabeçalhos de tamanhos diferentes */
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.fjc-title { font-size: 20px; font-weight: 800; color: #2c3e50; line-height: 1.3; margin-bottom: 10px; }
.fjc-gg-row { display: flex; justify-content: space-between; align-items: center; }
.fjc-gg { color: #1E56E0; font-weight: 700; font-size: 0.95rem; }
.fjc-score { color: white; font-weight: 700; padding: 4px 12px; border-radius: 12px; font-size: 0.9rem; }

/* METADADOS do Card */
.card-meta-block {
    background-color: white;
    padding: 15px 20px;
    border-bottom: 1px solid #eee;
    font-size: 0.85rem;
    color: #555;
    min-height: 100px; /* Garante altura mínima para metadados */
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.meta-row { display: flex; flex-wrap: wrap; gap: 15px; margin-bottom: 5px; }
.meta-item strong { color: #333; font-weight: 700; }

/* SEÇÕES DE CONTEÚDO (Role Description, Qualifications, etc.) */
/* CRUCIAL: height: 100% e flex-grow para alinhamento */
.card-section-block {
    background-color: #fdfdfd;
    border-left: 5px solid #ccc; /* Cor padrão */
    padding: 15px 20px;
    border-bottom: 1px solid #eee;
    display: flex;
    flex-direction: column;
    flex-grow: 1; /* Permite que o bloco cresça e ocupe espaço para alinhar */
    justify-content: flex-start; /* Alinha o conteúdo ao topo */
    min-height: 80px; /* Altura mínima para cada seção, ajustável */
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
    color: #333;
    line-height: 1.5;
    font-size: 0.9rem;
    white-space: pre-wrap; /* Mantém quebras de linha e formatação */
}
/* Estilo para a última seção de um card (remove border-bottom) */
.job-card-container > .card-section-block:last-of-type {
    border-bottom: none;
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

    # Normalização para evitar erros de chave
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

    # Texto rico (apenas campos distintivos para melhor match)
    df_jobs["Rich_Text"] = (
        df_jobs["Job Profile"] + ". " +
        df_jobs["Role Description"] + ". " +
        df_jobs["Grade Differentiator"] + ". " +
        df_jobs["Qualifications"] + ". " +
        df_jobs["Career Band Description"]
    )

    model = load_model()
    embeddings = model.encode(df_jobs["Rich_Text"].tolist(), show_progress_bar=True)

    return df_jobs, df_levels, embeddings

try:
    df, df_levels, job_embeddings = load_data_and_embeddings()
    model = load_model()
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}. Verifique se 'job_profile' e 'level_structure' existem no Excel e se as colunas estão corretas.")
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

    # Matching
    mask = (df["Job Family"] == selected_family) & (df["Sub Job Family"] == selected_subfamily)
    if not mask.any():
        st.error(f"Não foram encontrados cargos para a combinação '{selected_family}' e '{selected_subfamily}'.")
        st.stop()

    filtered_indices = df[mask].index
    if len(filtered_indices) == 0:
        st.error("Não há cargos com embeddings gerados para esta seleção. Verifique os dados.")
        st.stop()
        
    filtered_embeddings = job_embeddings[filtered_indices]
    query_emb = model.encode([desc_input])
    sims = cosine_similarity(query_emb, filtered_embeddings)[0]
    
    results = df.loc[filtered_indices].copy()
    results["similarity"] = sims
    top3 = results.sort_values("similarity", ascending=False).head(3)

    st.markdown("---")
    st.subheader("🏆 Cargos Mais Compatíveis")

    if len(top3) == 0:
        st.info("Nenhum cargo compatível encontrado para os critérios selecionados.")
        st.stop()
        
    # Prepara dados para renderização segura e Level Name
    rows_data = []
    for _, row_data in top3.iterrows():
        score_val = row_data["similarity"] * 100
        score_bg = "#28a745" if score_val > 85 else "#1E56E0" if score_val > 75 else "#fd7e14" if score_val > 60 else "#dc3545"
        
        # Busca Level Name de forma segura
        lvl_name = ""
        gg_val = str(row_data["Global Grade"]).strip()
        if not df_levels.empty and "Global Grade" in df_levels.columns and "Level Name" in df_levels.columns:
            match_level = df_levels[df_levels["Global Grade"].astype(str).str.strip() == gg_val]
            if not match_level.empty:
                lvl_name = f"• {match_level['Level Name'].iloc[0]}"
        
        rows_data.append({
            "data": row_data,
            "score_fmt": f"{score_val:.1f}%",
            "score_bg": score_bg,
            "lvl_name": lvl_name
        })

    # CRIA AS 3 COLUNAS PRINCIPAIS (onde cada coluna conterá um CARD COMPLETO)
    cols = st.columns(3)

    # Itera sobre as colunas e injeta o HTML completo de cada card
    for i, col in enumerate(cols):
        if i < len(rows_data):
            r = rows_data[i]
            d = r['data']

            # HTML para as seções, usando html.escape()
            sub_job_family_desc = f"""<div class="card-section-block" style="border-left-color: #95a5a6;">
                <div class="section-title" style="color: #7f8c8d;">🧭 Sub Job Family Description</div>
                <div class="section-content">{html.escape(str(d.get('Sub Job Family Description','-')))}</div>
            </div>"""
            
            job_profile_desc = f"""<div class="card-section-block" style="border-left-color: #e91e63;">
                <div class="section-title" style="color: #c2185b;">🧠 Job Profile Description</div>
                <div class="section-content">{html.escape(str(d.get('Job Profile Description','-')))}</div>
            </div>"""

            career_band_desc = f"""<div class="card-section-block" style="border-left-color: #673ab7;">
                <div class="section-title" style="color: #512da8;">🏛️ Career Band Description</div>
                <div class="section-content">{html.escape(str(d.get('Career Band Description','-')))}</div>
            </div>"""

            role_desc = f"""<div class="card-section-block" style="border-left-color: #1E56E0;">
                <div class="section-title" style="color: #0d47a1;">🎯 Role Description</div>
                <div class="section-content">{html.escape(str(d.get('Role Description','-')))}</div>
            </div>"""

            grade_diff = f"""<div class="card-section-block" style="border-left-color: #ff9800;">
                <div class="section-title" style="color: #e65100;">🏅 Grade Differentiator</div>
                <div class="section-content">{html.escape(str(d.get('Grade Differentiator','-')))}</div>
            </div>"""
            
            qualifications = ""
            if d.get('Qualifications') and str(d['Qualifications']).strip() not in ['-', '', 'nan']:
                qualifications = f"""<div class="card-section-block" style="border-left-color: #009688;">
                    <div class="section-title" style="color: #00796b;">🎓 Qualifications</div>
                    <div class="section-content">{html.escape(str(d['Qualifications']))}</div>
                </div>"""
            
            # Monta o card completo
            card_html = f"""
            <div class="job-card-container">
                <div class="card-header-block">
                    <div class="fjc-title">{html.escape(r['data']['Job Profile'])}</div>
                    <div class="fjc-gg-row">
                        <div class="fjc-gg">GG {r['data']['Global Grade']} {r['lvl_name']}</div>
                        <div class="fjc-score" style="background-color: {r['score_bg']};">{r['score_fmt']} Match</div>
                    </div>
                </div>

                <div class="card-meta-block">
                    <div class="meta-row">
                        <div class="meta-item"><strong>Família:</strong> {html.escape(str(d.get('Job Family','-')))}</div>
                    </div>
                    <div class="meta-row">
                        <div class="meta-item"><strong>Subfamília:</strong> {html.escape(str(d.get('Sub Job Family','-')))}</div>
                    </div>
                    <div class="meta-row">
                        <div class="meta-item"><strong>Carreira:</strong> {html.escape(str(d.get('Career Path','-')))}</div>
                        <div class="meta-item"><strong>Cód:</strong> {html.escape(str(d.get('Full Job Code','-')))}</div>
                    </div>
                </div>
                
                {sub_job_family_desc}
                {job_profile_desc}
                {career_band_desc}
                {role_desc}
                {grade_diff}
                {qualifications}
                
            </div>
            """
            col.markdown(card_html, unsafe_allow_html=True)
            
    if top3.iloc[0]["similarity"] < 0.6:
        st.info("💡 Aderência moderada. Tente refinar sua descrição com mais detalhes sobre o nível de senioridade e responsabilidades específicas.")
