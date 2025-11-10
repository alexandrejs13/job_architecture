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
# ESTILO
# ===========================================================
st.markdown("""
<style>
.block-container {max-width: 1200px !important;}
.stTextArea textarea {font-size: 16px !important;}
.match-card {
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    margin-bottom: 15px;
    border-left: 6px solid #ccc;
    transition: transform 0.2s;
}
.match-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
}
.match-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 10px;
}
.match-title {
    font-size: 22px;
    font-weight: 700;
    color: #2c3e50;
    margin: 0;
}
.match-score {
    font-size: 18px;
    font-weight: 800;
    padding: 4px 12px;
    border-radius: 20px;
    background-color: #f8f9fa;
}
.match-meta {
    color: #666;
    font-size: 0.95rem;
    margin-bottom: 15px;
    padding-bottom: 15px;
    border-bottom: 1px solid #eee;
}
.highlight-label {
    font-weight: 600;
    color: #1E56E0;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 5px;
    display: block;
}
.match-content {
    color: #444;
    font-size: 0.95rem;
    line-height: 1.5;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# ===========================================================
# CARREGAMENTO DE DADOS E MODELO
# ===========================================================
@st.cache_resource
def load_model():
    # Modelo leve e eficiente para português/multilíngue
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

@st.cache_data(show_spinner=False)
def load_data_and_embeddings():
    data = load_excel_data()
    df_jobs = data.get("job_profile", pd.DataFrame()).fillna("")
    # Garante que o índice é limpo para filtragem posterior
    df_jobs = df_jobs.reset_index(drop=True)
    
    levels = data.get("level_structure", pd.DataFrame()).fillna("")

    # Limpeza básica
    if not levels.empty and "Global Grade" in levels.columns:
         levels["Global Grade"] = levels["Global Grade"].astype(str).str.replace(r"\.0$", "", regex=True).str.strip()

    required = ["Job Family", "Sub Job Family", "Job Profile", "Role Description", 
                "Grade Differentiator", "Qualifications", "Global Grade", "Career Path"]
    for c in required:
        if c not in df_jobs.columns: df_jobs[c] = ""
    
    df_jobs["Global Grade"] = df_jobs["Global Grade"].astype(str).str.replace(r"\.0$", "", regex=True).str.strip()

    # Criação do texto rico para matching
    df_jobs["Rich_Text"] = (
        df_jobs["Job Profile"] + ". " +
        df_jobs["Role Description"] + ". " +
        df_jobs["Grade Differentiator"] + ". " +
        df_jobs["Qualifications"]
    )

    # Gera embeddings uma vez e armazena em cache
    model = load_model()
    embeddings = model.encode(df_jobs["Rich_Text"].tolist(), show_progress_bar=True)

    return df_jobs, levels, embeddings

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
st.markdown("Encontre o cargo mais adequado com base nas responsabilidades e requisitos.")

# --- Filtros ---
c1, c2, c3 = st.columns([1.5, 1.5, 3])
with c1:
    families = sorted(df["Job Family"].unique())
    selected_family = st.selectbox("📂 Família", ["Todas"] + families)
with c2:
    subfamilies = []
    if selected_family != "Todas":
        subfamilies = sorted(df[df["Job Family"] == selected_family]["Sub Job Family"].unique())
    selected_subfamily = st.selectbox("📂 Subfamília", ["Todas"] + subfamilies)
with c3:
    # Espaço vazio para alinhamento ou futuro uso
    pass

# --- Input de Texto ---
desc_input = st.text_area(
    "📋 Cole aqui a descrição do cargo (quanto mais detalhes, melhor):",
    height=250,
    placeholder="Ex: Profissional responsável por liderar projetos de transformação digital, com foco em automação de processos financeiros. Necessário experiência com SAP, gestão de stakeholders internacionais e inglês fluente. Atuação sênior, reportando ao Diretor."
)

col_btn, _ = st.columns([1, 4])
with col_btn:
    run_match = st.button("🔍 Analisar Aderência", type="primary", use_container_width=True)

# ===========================================================
# LÓGICA DE MATCHING
# ===========================================================
if run_match:
    if len(desc_input.strip().split()) < 10:
        st.warning("⚠️ A descrição está muito curta. Adicione mais detalhes para um bom resultado.")
        st.stop()

    # 1. Filtragem Inteligente (Cria uma máscara booleana)
    mask = pd.Series([True] * len(df))
    if selected_family != "Todas":
        mask &= (df["Job Family"] == selected_family)
    if selected_subfamily != "Todas":
        mask &= (df["Sub Job Family"] == selected_subfamily)

    if not mask.any():
        st.error("Nenhum cargo encontrado para os filtros selecionados.")
        st.stop()

    # 2. Seleciona apenas os embeddings que passaram no filtro
    # Isso é crucial: filtra os dados E os vetores pré-calculados
    filtered_indices = df[mask].index
    filtered_embeddings = job_embeddings[filtered_indices]

    # 3. Calcula similaridade apenas no subconjunto filtrado (RÁPIDO!)
    query_emb = model.encode([desc_input])
    sims = cosine_similarity(query_emb, filtered_embeddings)[0]

    # 4. Prepara resultados
    results = df.loc[filtered_indices].copy()
    results["similarity"] = sims
    top_results = results.sort_values("similarity", ascending=False).head(5)

    # ===========================================================
# EXIBIÇÃO DOS RESULTADOS
# ===========================================================
    st.markdown("---")
    st.subheader("🏆 Top 5 Cargos Compatíveis")
    
    for i, (idx, row) in enumerate(top_results.iterrows()):
        score = row["similarity"] * 100
        
        # Cores dinâmicas baseadas na trilha e no score
        if score > 85: score_color = "#28a745"
        elif score > 70: score_color = "#1E56E0"
        elif score > 50: score_color = "#fd7e14"
        else: score_color = "#dc3545"

        path_lower = str(row['Career Path']).lower()
        if "manage" in path_lower or "executive" in path_lower: border_color = "var(--blue)"
        elif "professional" in path_lower: border_color = "var(--green)"
        elif "techni" in path_lower: border_color = "var(--orange)"
        else: border_color = "#999"

        # Nome do nível (se disponível)
        level_name = ""
        if not df_levels.empty and "Global Grade" in df_levels.columns:
             match = df_levels[df_levels["Global Grade"] == row["Global Grade"]]
             if not match.empty:
                 level_name = f" • {match.iloc[0]['Level Name']}"

        # Card Principal
        st.markdown(f"""
        <div class="match-card" style="border-left-color: {border_color}">
            <div class="match-header">
                <h3 class="match-title">{i+1}. {row['Job Profile']}</h3>
                <div class="match-score" style="color: {score_color}">{score:.0f}% Aderência</div>
            </div>
            <div class="match-meta">
                GG {row['Global Grade']}{level_name} | 📂 {row['Job Family']} &rsaquo; {row['Sub Job Family']} | 🛤️ {row['Career Path']}
            </div>
            <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 300px;">
                    <span class="highlight-label">🎯 Descrição do Papel</span>
                    <div class="match-content">{row['Role Description'][:300] + '...' if len(row['Role Description']) > 300 else row['Role Description']}</div>
                </div>
                <div style="flex: 1; min-width: 300px;">
                     <span class="highlight-label">🏅 Diferencial de Nível</span>
                     <div class="match-content">{row['Grade Differentiator'][:300] + '...' if len(row['Grade Differentiator']) > 300 else row['Grade Differentiator']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Detalhes Expansíveis
        with st.expander(f"📄 Ver detalhes completos de: {row['Job Profile']}"):
            cA, cB = st.columns(2)
            with cA:
                st.markdown("**Descrição Completa:**")
                st.write(row['Role Description'])
                st.markdown("**Diferencial de Nível:**")
                st.write(row['Grade Differentiator'])
            with cB:
                st.markdown("**Qualificações:**")
                st.write(row['Qualifications'])
                st.markdown("**KPIs / Parâmetros:**")
                st.write(row.get('KPIs / Specific Parameters', '-'))
