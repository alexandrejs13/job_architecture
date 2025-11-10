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
# ESTILO (LAYOUT MAIS LIMPO E DIRETO)
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
    border-left: 8px solid #ccc; /* Cor default */
    transition: transform 0.2s;
}
.match-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}
.match-score {
    font-size: 24px;
    font-weight: 800;
    color: #333;
    float: right;
}
.match-title {
    font-size: 20px;
    font-weight: 700;
    color: #1E56E0;
    margin-bottom: 5px;
}
.match-meta {
    color: #666;
    font-size: 0.9rem;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# ===========================================================
# CARREGAMENTO DE DADOS E MODELO (ROBUSTO)
# ===========================================================
@st.cache_resource
def load_model():
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

@st.cache_data(show_spinner=False)
def load_data_and_embeddings():
    data = load_excel_data()
    df_jobs = data.get("job_profile", pd.DataFrame()).fillna("")
    df_levels = data.get("level_structure", pd.DataFrame()).fillna("")

    # 1. LIMPEZA CRÍTICA DE COLUNAS (Remove espaços extras que causam KeyError)
    if not df_jobs.empty:
        df_jobs.columns = df_jobs.columns.str.strip()
    if not df_levels.empty:
        df_levels.columns = df_levels.columns.str.strip()

    # 2. GARANTIA DE COLUNAS NECESSÁRIAS
    required_cols = ["Job Family", "Sub Job Family", "Job Profile", "Role Description", 
                     "Grade Differentiator", "KPIs / Specific Parameters", "Qualifications", "Global Grade", "Career Path"]
    for c in required_cols:
        if c not in df_jobs.columns: df_jobs[c] = ""

    # 3. PADRONIZAÇÃO DO GLOBAL GRADE (para garantir o match entre as planilhas)
    # Converte para string, remove decimais (.0) e espaços
    df_jobs["Global Grade"] = df_jobs["Global Grade"].astype(str).str.replace(r"\.0$", "", regex=True).str.strip()
    if not df_levels.empty and "Global Grade" in df_levels.columns:
         df_levels["Global Grade"] = df_levels["Global Grade"].astype(str).str.replace(r"\.0$", "", regex=True).str.strip()

    # 4. CRIAÇÃO DO TEXTO RICO PARA O MODELO
    df_jobs["Rich_Text"] = (
        "Cargo: " + df_jobs["Job Profile"] + ". " +
        "Família: " + df_jobs["Job Family"] + ". " +
        "Descrição: " + df_jobs["Role Description"] + ". " +
        "Diferencial: " + df_jobs["Grade Differentiator"] + ". " +
        "Requisitos: " + df_jobs["Qualifications"]
    )

    # 5. GERAÇÃO DOS EMBEDDINGS (Cacheado)
    model = load_model()
    embeddings = model.encode(df_jobs["Rich_Text"].tolist(), show_progress_bar=True)

    return df_jobs, df_levels, embeddings

# Carrega tudo
try:
    df, levels, job_embeddings = load_data_and_embeddings()
    model = load_model()
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

# ===========================================================
# INTERFACE
# ===========================================================
section("🧩 Job Match")
st.markdown("Descreva as responsabilidades e requisitos do cargo para encontrar a melhor correspondência na arquitetura.")

col1, col2 = st.columns([1, 2])

with col1:
    st.write("##### 🎯 Filtros (Opcional)")
    families = sorted(df["Job Family"].unique())
    selected_family = st.selectbox("Família", ["Todas"] + families)
    
    subfamilies = []
    if selected_family != "Todas":
        subfamilies = sorted(df[df["Job Family"] == selected_family]["Sub Job Family"].unique())
    selected_subfamily = st.selectbox("Subfamília", ["Todas"] + subfamilies)
    
    st.info("📝 **Dica:** Quanto mais detalhada a descrição (incluindo nível de senioridade, escopo de gestão, etc.), melhor será o resultado.")

with col2:
    desc_input = st.text_area(
        "Cole aqui a descrição do cargo:",
        height=300,
        placeholder="Exemplo: Responsável por liderar a estratégia de vendas digitais, gerenciando uma equipe de 5 especialistas. Necessário forte background em analytics, growth marketing e experiência prévia com gestão de budget de mídia..."
    )
    
    btn_match = st.button("🔍 Analisar Aderência", type="primary", use_container_width=True)

# ===========================================================
# LÓGICA DE MATCHING E EXIBIÇÃO
# ===========================================================
if btn_match:
    if len(desc_input.strip()) < 20:
        st.warning("⚠️ Por favor, insira uma descrição mais detalhada (mínimo 20 caracteres) para uma análise precisa.")
        st.stop()

    # 1. Filtra o DataFrame base se necessário
    mask = pd.Series([True] * len(df))
    if selected_family != "Todas": mask &= (df["Job Family"] == selected_family)
    if selected_subfamily != "Todas": mask &= (df["Sub Job Family"] == selected_subfamily)

    if not mask.any():
        st.error("Nenhum cargo encontrado para os filtros selecionados.")
        st.stop()

    # 2. Calcula similaridade apenas para os itens filtrados
    filtered_indices = df[mask].index
    filtered_embeddings = job_embeddings[filtered_indices]
    query_embedding = model.encode([desc_input])
    similarities = cosine_similarity(query_embedding, filtered_embeddings)[0]

    # 3. Prepara os resultados
    results = df.loc[filtered_indices].copy()
    results["similarity"] = similarities
    top_results = results.sort_values("similarity", ascending=False).head(5)

    # 4. Exibe os resultados
    st.markdown("### 🏆 Top 5 Cargos Compatíveis")
    
    for i, (idx, row) in enumerate(top_results.iterrows()):
        score = row["similarity"] * 100
        
        # Cor da borda baseada no score
        if score >= 85: border_color = "#28a745" # Verde (Excelente)
        elif score >= 70: border_color = "#1E56E0" # Azul (Bom)
        elif score >= 50: border_color = "#fd7e14" # Laranja (Médio)
        else: border_color = "#dc3545" # Vermelho (Baixo)

        # Tenta buscar o nome do nível de forma segura
        level_name = ""
        if not levels.empty and "Global Grade" in levels.columns and "Level Name" in levels.columns:
            match = levels[levels["Global Grade"] == row["Global Grade"]]
            if not match.empty:
                level_name = f" • {match.iloc[0]['Level Name']}"

        # Renderiza o card simplificado
        st.markdown(f"""
        <div class="match-card" style="border-left-color: {border_color}">
            <div class="match-score" style="color: {border_color}">{score:.0f}%</div>
            <div class="match-title">{row['Job Profile']}</div>
            <div class="match-meta">
                GG {row['Global Grade']}{level_name} | 📂 {row['Job Family']} &rsaquo; {row['Sub Job Family']} | 🛤️ {row['Career Path']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Expander nativo do Streamlit para detalhes (mais limpo que jogar tudo na tela)
        with st.expander(f"📄 Ver detalhes do cargo #{i+1}"):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**🎯 Descrição do Papel:**")
                st.write(row["Role Description"] if row["Role Description"] else "_Não informado_")
                st.markdown("**🏅 Diferencial de Nível:**")
                st.write(row["Grade Differentiator"] if row["Grade Differentiator"] else "_Não informado_")
            with c2:
                st.markdown("**🎓 Requisitos:**")
                st.write(row["Qualifications"] if row["Qualifications"] else "_Não informado_")
                st.markdown("**📊 KPIs / Parâmetros:**")
                st.write(row["KPIs / Specific Parameters"] if row["KPIs / Specific Parameters"] else "_Não informado_")
