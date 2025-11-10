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
# ESTILO (ADAPTADO PARA ALINHAMENTO PERFEITO)
# ===========================================================
st.markdown("""
<style>
.block-container {
    max-width: 95% !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}
.stTextArea textarea {font-size: 16px !important;}

/* --- BLOCOS DE CONTEÚDO (PARA ALINHAMENTO) --- */
/* Cada seção do card será um bloco independente visualmente conectado */

.card-header-block {
    background-color: #f8f9fa;
    border: 1px solid #e0e0e0;
    border-bottom: none;
    border-radius: 12px 12px 0 0;
    padding: 20px;
    height: 100%; /* Força altura igual na linha */
}

.card-meta-block {
    background-color: white;
    border: 1px solid #e0e0e0;
    border-top: 1px solid #eee;
    border-bottom: none;
    padding: 15px 20px;
    font-size: 0.85rem;
    color: #555;
    height: 100%;
}

.card-section-block {
    background-color: white;
    border-left: 5px solid #ccc; /* Cor padrão, será sobrescrita */
    border-right: 1px solid #e0e0e0;
    border-bottom: 1px solid #eee; /* Linha divisória suave entre seções */
    padding: 15px 20px;
    height: 100%; /* CRUCIAL PARA O ALINHAMENTO */
    display: flex;
    flex-direction: column;
}

.card-footer-block {
    background-color: white;
    border: 1px solid #e0e0e0;
    border-top: none;
    border-radius: 0 0 12px 12px;
    padding: 5px; /* Apenas para fechar o card visualmente */
}

/* TIPOGRAFIA INTERNA */
.fjc-title { font-size: 20px; font-weight: 800; color: #2c3e50; line-height: 1.3; margin-bottom: 10px; }
.fjc-gg-row { display: flex; justify-content: space-between; align-items: center; }
.fjc-gg { color: #1E56E0; font-weight: 700; }
.fjc-score { color: white; font-weight: 700; padding: 4px 12px; border-radius: 12px; font-size: 0.9rem; }

.section-title { font-weight: 700; font-size: 0.95rem; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }
.section-content { color: #333; line-height: 1.5; font-size: 0.9rem; white-space: pre-wrap; }

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
        # Garante todas as colunas necessárias
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

    # Limpeza de GG
    df_jobs["Global Grade"] = df_jobs["Global Grade"].astype(str).str.replace(r"\.0$", "", regex=True).str.strip()
    if "Global Grade" in df_levels.columns:
        df_levels["Global Grade"] = df_levels["Global Grade"].astype(str).str.replace(r"\.0$", "", regex=True).str.strip()
    
    # Texto rico (apenas campos distintivos para melhor match)
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
    height=200,
    placeholder="Descreva as principais responsabilidades, escopo de atuação, nível de autonomia..."
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
    # RENDERIZAÇÃO ALINHADA (LINHA POR LINHA)
    # ===========================================================
    st.markdown("---")
    st.subheader("🏆 Cargos Mais Compatíveis")

    if len(top3) < 3:
        st.warning("Menos de 3 cargos encontrados para comparação.")

    # Prepara dados para renderização segura
    rows = []
    for _, row_data in top3.iterrows():
        # Score & Cores
        score_val = row_data["similarity"] * 100
        score_bg = "#28a745" if score_val > 85 else "#1E56E0" if score_val > 75 else "#fd7e14" if score_val > 60 else "#dc3545"
        
        # Level Name Seguro
        lvl_name = ""
        if not df_levels.empty and "Global Grade" in df_levels.columns and "Level Name" in df_levels.columns:
            # Conversão explícita para string e strip para garantir match
            gg_val = str(row_data["Global Grade"]).strip()
            match = df_levels[df_levels["Global Grade"].astype(str).str.strip() == gg_val]
            if not match.empty:
                lvl_name = f"• {match['Level Name'].iloc[0]}"
        
        rows.append({
            "data": row_data,
            "score_fmt": f"{score_val:.1f}%",
            "score_bg": score_bg,
            "lvl_name": lvl_name
        })

    # --- CRIA AS 3 COLUNAS PRINCIPAIS ---
    cols = st.columns(3)

    # 1. LINHA DE CABEÇALHO (Título, GG, Score)
    for i, col in enumerate(cols):
        if i < len(rows):
            r = rows[i]
            col.markdown(f"""
            <div class="card-header-block">
                <div class="fjc-title">{html.escape(r['data']['Job Profile'])}</div>
                <div class="fjc-gg-row">
                    <div class="fjc-gg">GG {r['data']['Global Grade']} {r['lvl_name']}</div>
                    <div class="fjc-score" style="background-color: {r['score_bg']};">{r['score_fmt']} Match</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # 2. LINHA DE METADADOS
    for i, col in enumerate(cols):
        if i < len(rows):
            d = rows[i]['data']
            col.markdown(f"""
            <div class="card-meta-block">
                <div><strong>Família:</strong> {html.escape(str(d.get('Job Family','-')))}</div>
                <div><strong>Subfamília:</strong> {html.escape(str(d.get('Sub Job Family','-')))}</div>
                <div><strong>Carreira:</strong> {html.escape(str(d.get('Career Path','-')))}</div>
                <div><strong>Cód:</strong> {html.escape(str(d.get('Full Job Code','-')))}</div>
            </div>
            """, unsafe_allow_html=True)

    # 3. LINHA: Sub Job Family Description (Cinza)
    for i, col in enumerate(cols):
        if i < len(rows):
            col.markdown(f"""
            <div class="card-section-block" style="border-left-color: #95a5a6;">
                <div class="section-title" style="color: #7f8c8d;">🧭 Sub Job Family Description</div>
                <div class="section-content">{html.escape(str(rows[i]['data'].get('Sub Job Family Description','-')))}</div>
            </div>
            """, unsafe_allow_html=True)

    # 4. LINHA: Job Profile Description (Rosa)
    for i, col in enumerate(cols):
        if i < len(rows):
            col.markdown(f"""
            <div class="card-section-block" style="border-left-color: #e91e63;">
                <div class="section-title" style="color: #c2185b;">🧠 Job Profile Description</div>
                <div class="section-content">{html.escape(str(rows[i]['data'].get('Job Profile Description','-')))}</div>
            </div>
            """, unsafe_allow_html=True)

    # 5. LINHA: Career Band Description (Roxo)
    for i, col in enumerate(cols):
        if i < len(rows):
            col.markdown(f"""
            <div class="card-section-block" style="border-left-color: #673ab7;">
                <div class="section-title" style="color: #512da8;">🏛️ Career Band Description</div>
                <div class="section-content">{html.escape(str(rows[i]['data'].get('Career Band Description','-')))}</div>
            </div>
            """, unsafe_allow_html=True)

    # 6. LINHA: Role Description (Azul)
    for i, col in enumerate(cols):
        if i < len(rows):
            col.markdown(f"""
            <div class="card-section-block" style="border-left-color: #1E56E0;">
                <div class="section-title" style="color: #0d47a1;">🎯 Role Description</div>
                <div class="section-content">{html.escape(str(rows[i]['data'].get('Role Description','-')))}</div>
            </div>
            """, unsafe_allow_html=True)

    # 7. LINHA: Grade Differentiator (Laranja)
    for i, col in enumerate(cols):
        if i < len(rows):
            col.markdown(f"""
            <div class="card-section-block" style="border-left-color: #ff9800;">
                <div class="section-title" style="color: #e65100;">🏅 Grade Differentiator</div>
                <div class="section-content">{html.escape(str(rows[i]['data'].get('Grade Differentiator','-')))}</div>
            </div>
            """, unsafe_allow_html=True)

    # 8. LINHA: Qualifications (Verde)
    for i, col in enumerate(cols):
        if i < len(rows):
            qual = str(rows[i]['data'].get('Qualifications','-'))
            # Só mostra se tiver conteúdo real
            if len(qual) > 5 and qual.lower() != 'nan':
                 col.markdown(f"""
                <div class="card-section-block" style="border-left-color: #009688;">
                    <div class="section-title" style="color: #00796b;">🎓 Qualifications</div>
                    <div class="section-content">{html.escape(qual)}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                 # Mantém o alinhamento mesmo se vazio
                 col.markdown('<div class="card-section-block" style="border:none; background:transparent;"></div>', unsafe_allow_html=True)

    # 9. RODAPÉ DO CARD (Fechamento Visual)
    for i, col in enumerate(cols):
        if i < len(rows):
            col.markdown('<div class="card-footer-block"></div>', unsafe_allow_html=True)

    if top3.iloc[0]["similarity"] < 0.6:
        st.info("💡 Aderência moderada. Tente refinar sua descrição.")
