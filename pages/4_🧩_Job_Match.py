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
/* Estilo dos Cards de Resultado */
.match-card {
    background-color: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    margin-bottom: 20px;
    border-left: 8px solid #ccc;
    transition: all 0.3s ease;
}
.match-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.12);
}
.match-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 15px;
    border-bottom: 1px solid #eee;
    padding-bottom: 15px;
}
.match-title {
    font-size: 24px;
    font-weight: 700;
    color: #2c3e50;
    margin: 0;
}
.match-score {
    font-size: 20px;
    font-weight: 800;
    padding: 6px 15px;
    border-radius: 30px;
    background-color: #f8f9fa;
    white-space: nowrap;
}
.match-meta {
    color: #555;
    font-size: 1rem;
    margin-bottom: 20px;
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
}
.meta-tag {
    background: #f0f2f6;
    padding: 4px 10px;
    border-radius: 6px;
    font-weight: 500;
}
.highlight-label {
    font-weight: 700;
    color: #1E56E0;
    font-size: 0.95rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 8px;
    display: block;
}
.match-content {
    color: #333;
    font-size: 1rem;
    line-height: 1.6;
    background: #fcfcfc;
    padding: 15px;
    border-radius: 8px;
    border: 1px solid #f0f0f0;
}
</style>
""", unsafe_allow_html=True)

# ===========================================================
# CARREGAMENTO DE DADOS E MODELO (COM CORREÇÃO DE ERRO)
# ===========================================================
@st.cache_resource
def load_model():
    # Modelo multilíngue robusto para entender contexto hierárquico mesmo em inglês/português misturado
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

@st.cache_data(show_spinner=False)
def load_data_and_embeddings():
    data = load_excel_data()
    df_jobs = data.get("job_profile", pd.DataFrame()).fillna("")
    df_levels = data.get("level_structure", pd.DataFrame()).fillna("")

    # --- CORREÇÃO PROATIVA DO KEYERROR ---
    # Normaliza nomes das colunas (remove espaços extras que causam o erro)
    if not df_jobs.empty:
        df_jobs.columns = df_jobs.columns.str.strip()
    if not df_levels.empty:
        df_levels.columns = df_levels.columns.str.strip()

    # Garante que as colunas essenciais existam, mesmo que vazias
    required_cols = ["Job Family", "Sub Job Family", "Job Profile", "Role Description", 
                     "Grade Differentiator", "Qualifications", "Global Grade", "Career Path"]
    for c in required_cols:
        if c not in df_jobs.columns: df_jobs[c] = ""
    
    # Padronização do Global Grade para matching
    df_jobs["Global Grade"] = df_jobs["Global Grade"].astype(str).str.replace(r"\.0$", "", regex=True).str.strip()
    if "Global Grade" in df_levels.columns:
         df_levels["Global Grade"] = df_levels["Global Grade"].astype(str).str.replace(r"\.0$", "", regex=True).str.strip()

    # Criação do "Rich Text" para o modelo entender a hierarquia
    # Adicionamos prefixos em inglês (já que a base é em inglês) para ajudar o modelo
    df_jobs["Rich_Text"] = (
        "Job Profile: " + df_jobs["Job Profile"] + ". " +
        "Role Description: " + df_jobs["Role Description"] + ". " +
        "Grade Differentiator (Seniority Level): " + df_jobs["Grade Differentiator"] + ". " +
        "Requirements: " + df_jobs["Qualifications"]
    )

    model = load_model()
    embeddings = model.encode(df_jobs["Rich_Text"].tolist(), show_progress_bar=True)

    return df_jobs, df_levels, embeddings

try:
    df, df_levels, job_embeddings = load_data_and_embeddings()
    model = load_model()
except Exception as e:
    st.error(f"Erro crítico ao carregar dados. Verifique as planilhas: {e}")
    st.stop()

# ===========================================================
# INTERFACE
# ===========================================================
section("🧩 Job Match")
st.markdown(" utilize nossa IA para encontrar o cargo ideal na estrutura global.")

# --- Filtros ---
c1, c2 = st.columns(2)
with c1:
    families = sorted(df["Job Family"].unique())
    selected_family = st.selectbox("📂 Família (Obrigatório)", ["Selecione..."] + families)
with c2:
    subfamilies = []
    if selected_family != "Selecione...":
        subfamilies = sorted(df[df["Job Family"] == selected_family]["Sub Job Family"].unique())
    selected_subfamily = st.selectbox("📂 Subfamília (Obrigatório)", ["Selecione..."] + subfamilies)

# --- Input de Texto ---
desc_input = st.text_area(
    "📋 Descreva as responsabilidades e requisitos (Mínimo 50 palavras):",
    height=300,
    placeholder="Para uma análise precisa, detalhe: \n1. Principais responsabilidades (o que faz, escopo global/local)\n2. Nível de autonomia e tomada de decisão\n3. Gestão de pessoas (se aplicável)\n4. Requisitos técnicos e experiência necessária..."
)

# Contagem de palavras em tempo real (aproximada)
word_count = len(desc_input.strip().split())
st.caption(f"Contagem de palavras: {word_count} / 50")

col_btn, _ = st.columns([1, 2])
with col_btn:
    run_match = st.button("🔍 Analisar Aderência", type="primary", use_container_width=True)

# ===========================================================
# LÓGICA DE VALIDAÇÃO E MATCHING
# ===========================================================
if run_match:
    # --- VALIDAÇÃO RIGOROSA (REQUISITO 1) ---
    errors = []
    if selected_family == "Selecione...":
        errors.append("• Selecionar a **Família** de cargos.")
    if selected_subfamily == "Selecione...":
        errors.append("• Selecionar a **Subfamília** correspondente.")
    if word_count < 50:
        errors.append(f"• Fornecer mais detalhes na descrição (faltam aproximadamente **{50 - word_count}** palavras).")
    
    if errors:
        st.warning(
            "#### ⚠️ Para garantir a precisão da nossa análise de IA:\n\n"
            "Por favor, complete os seguintes requisitos antes de continuar:\n" + 
            "\n".join(errors)
        )
        st.stop()

    # --- FILTRAGEM ---
    mask = (df["Job Family"] == selected_family) & (df["Sub Job Family"] == selected_subfamily)
    if not mask.any():
        st.error("Não foram encontrados cargos para esta combinação de Família e Subfamília.")
        st.stop()

    # --- MATCHING ---
    filtered_indices = df[mask].index
    filtered_embeddings = job_embeddings[filtered_indices]
    query_emb = model.encode([desc_input])
    sims = cosine_similarity(query_emb, filtered_embeddings)[0]

    results = df.loc[filtered_indices].copy()
    results["similarity"] = sims
    top_results = results.sort_values("similarity", ascending=False).head(3) # Top 3 é o ideal

    # ===========================================================
    # EXIBIÇÃO DOS RESULTADOS
    # ===========================================================
    st.markdown("---")
    st.subheader("🏆 Cargos Mais Compatíveis Encontrados")
    
    for i, (idx, row) in enumerate(top_results.iterrows()):
        score = row["similarity"] * 100
        
        # Cores baseadas no score
        if score > 85: score_color, border_color = "#28a745", "#28a745" # Verde
        elif score > 75: score_color, border_color = "#1E56E0", "#1E56E0" # Azul
        elif score > 60: score_color, border_color = "#fd7e14", "#fd7e14" # Laranja
        else: score_color, border_color = "#dc3545", "#dc3545" # Vermelho

        # Busca segura do Level Name (CORREÇÃO DO KEYERROR)
        level_name_display = ""
        if not df_levels.empty and "Global Grade" in df_levels.columns and "Level Name" in df_levels.columns:
             match_level = df_levels[df_levels["Global Grade"] == row["Global Grade"]]
             if not match_level.empty:
                 # Usa .iloc[0] para pegar o primeiro valor de forma segura
                 level_name_display = f"• {match_level['Level Name'].iloc[0]}"

        # Card Principal
        st.markdown(f"""
        <div class="match-card" style="border-left-color: {border_color}">
            <div class="match-header">
                <h3 class="match-title">#{i+1} {row['Job Profile']}</h3>
                <div class="match-score" style="color: {score_color}">{score:.0f}% Match</div>
            </div>
            <div class="match-meta">
                <span class="meta-tag">🏛️ GG {row['Global Grade']} {level_name_display}</span>
                <span class="meta-tag">🛤️ {row['Career Path']}</span>
            </div>
            <div style="display: flex; gap: 25px; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 300px;">
                    <span class="highlight-label">🎯 Descrição do Papel</span>
                    <div class="match-content">{row['Role Description']}</div>
                </div>
                <div style="flex: 1; min-width: 300px;">
                     <span class="highlight-label">🏅 Diferencial de Senioridade (GG {row['Global Grade']})</span>
                     <div class="match-content" style="background: #f0f7ff; border-color: #cce5ff;">
                        {row['Grade Differentiator']}
                     </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Aviso se o melhor score for baixo mesmo com os requisitos atendidos
    if top_results.iloc[0]["similarity"] < 0.6:
        st.info("ℹ️ **Dica de Otimização:** A aderência encontrada foi moderada. Tente incluir mais palavras-chave específicas da área técnica ou de gestão na sua descrição para refinar o resultado.")
