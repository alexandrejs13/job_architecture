# -*- coding: utf-8 -*-
# pages/5_🧩_Job_Match.py

import streamlit as st
import pandas as pd
import html
import json
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
from utils.data_loader import load_excel_data
from utils.ui_components import lock_sidebar
from utils.ui import setup_sidebar
import re
import numpy as np

# ===========================================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ===========================================================
st.set_page_config(
    page_title="Job Match GGS Estruturado",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================================================
# 2. CSS GLOBAL (Manutenção do layout original)
# ===========================================================
css_path = Path(__file__).parents[1] / "assets" / "header.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
<style>
.page-header {
    background-color: #145efc;
    color: white;
    font-weight: 750;
    font-size: 1.35rem;
    border-radius: 12px;
    padding: 22px 36px;
    display: flex;
    align-items: center;
    gap: 18px;
    width: 100%;
    margin-bottom: 40px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.page-header img { width: 48px; height: 48px; }

[data-testid="stAppViewContainer"] {
    background-color: #f5f3f0;
    color: #202020;
    font-family: "Source Sans Pro","Helvetica",sans-serif;
}
.block-container {
    max-width: 95% !important; 
    padding-left: 1rem !important; 
    padding-right: 1rem !important;
}

/* ============ ESTILO DE GRID IDÊNTICO AO JOB PROFILE DESCRIPTION ============ */
.comparison-grid {
    display: grid;
    gap: 20px;
    margin-top: 20px;
}
.grid-cell {
    background: #fff;
    border: 1px solid #e0e0e0;
    padding: 15px;
    display: flex;
    flex-direction: column;
}
.header-cell {
    background: #f8f9fa;
    border-radius: 12px 12px 0 0;
    border-bottom: none;
}
.fjc-title { 
    font-size: 18px; 
    font-weight: 800; 
    color: #2c3e50; 
    margin-bottom: 2px;
    min-height: 50px; 
}
.fjc-gg-row { display: flex; justify-content: space-between; align-items: center; }
.fjc-gg { color: #145efc; font-weight: 700; }
.fjc-score { color: #145efc; font-weight: 700; padding: 4px 10px; border-radius: 12px; font-size: 0.9rem; } 
.meta-cell {
    border-top: 1px solid #eee;
    border-bottom: 1px solid #eee;
    font-size: 0.85rem;
    color: #555;
    min-height: 120px;
}
.meta-row { margin-bottom: 5px; }
.section-cell {
    border-left-width: 5px;
    border-left-style: solid;
    border-top: none;
    background: #fdfdfd;
}
.section-title { font-weight: 700; font-size: 0.95rem; margin-bottom: 8px; color: #333; display: flex; align-items: center; gap: 5px;}
.section-content { color: #444; font-size: 0.9rem; line-height: 1.5; white-space: pre-wrap; }
.footer-cell {
    height: 10px;
    border-top: none;
    border-radius: 0 0 12px 12px;
    background: #fff;
}
.ai-insight-box {
    background-color: #eef6fc;
    border-left: 5px solid #145efc;
    padding: 15px 20px;
    border-radius: 8px;
    margin: 20px 0;
    color: #2c3e50;
}
.ai-insight-title {
    font-weight: 800;
    color: #145efc;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 5px;
}
/* Estilo customizado para o alerta de erro (substitui st.error) */
.custom-error-box {
    border-left: 5px solid #d93025; /* Vermelho do Streamlit */
    background-color: #ffecec; /* Fundo levemente vermelho */
    padding: 15px 20px;
    border-radius: 8px;
    margin: 20px 0;
    color: #2c3e50;
}
.custom-error-title {
    font-weight: 800;
    color: #d93025;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 5px;
    font-size: 1rem;
}
</style>

<div class="page-header">
  <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/checkmark%20success.png" alt="icon">
  Análise de Aderência de Cargo (Filtro Estruturado GGS)
</div>
""", unsafe_allow_html=True)

setup_sidebar()
lock_sidebar()

# ===========================================================
# 3. FUNÇÕES AUXILIARES E CARREGAMENTO DE DADOS E MODELO
# ===========================================================

def sanitize_columns(df):
    """Converte nomes de colunas para snake_case e remove caracteres especiais."""
    cols = {}
    for col in df.columns:
        new_col = re.sub(r'[ /-]+', '_', col.strip())
        new_col = re.sub(r'[^\w_]', '', new_col).lower()
        cols[col] = new_col
    return df.rename(columns=cols)

@st.cache_resource
def load_model():
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

@st.cache_data
def load_json_rules():
    path = Path("wtw_match_rules.json") 
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"thresholds": {"weak_match": 0.50}, "wtw_reporting_limits": {}} # Default fallback

@st.cache_data
def load_data():
    """Carrega os dados e cria a coluna Global Grade Num."""
    try:
        data = load_excel_data() 
    except NameError:
        data = {"job_profile": pd.DataFrame(), "level_structure": pd.DataFrame()}

    df_jobs = sanitize_columns(data.get("job_profile", pd.DataFrame())).fillna("")
    df_levels = sanitize_columns(data.get("level_structure", pd.DataFrame())).fillna("")
    
    if "global_grade" in df_jobs.columns:
        df_jobs["global_grade_num"] = pd.to_numeric(df_jobs["global_grade"], errors="coerce").fillna(0).astype(int)
    else:
        df_jobs["global_grade_num"] = 0 
    
    return df_jobs, df_levels

df, df_levels = load_data()
model = load_model()
JOB_RULES = load_json_rules()

GG_LIMITS_MAP = JOB_RULES.get("wtw_reporting_limits", {})

# ===========================================================
# 4. FUNÇÃO DE CÁLCULO DE MATCH BASEADO EM PARÂMETROS
# ===========================================================

def calculate_structured_match(df_filtered, params):
    """
    Calcula a pontuação de aderência (similarity) baseado nos inputs estruturados GGS.
    O GG Alvo é inferido pelo Score dos Fatores para ranquear os cargos.
    """
    if df_filtered.empty:
        return pd.DataFrame()

    # Ponderadores para os fatores
    weights = {
        'knowledge_level': 0.35,  # Conhecimento
        'problem_level': 0.30,    # Solução de Problemas
        'leadership_scope': 0.20, # Liderança
        'impact_scope': 0.15      # Área de Impacto
    }
    
    # Mapeamento de Nível para um Score Numérico (1 a 3, simulando a progressão GGS)
    knowledge_map = {"Rotinas/Procedimentos Definidos (Banda U/W)": 1, "Conhecimento de Conceitos e Princípios (Banda P/T)": 2, "Domínio Amplo e Integrado da Disciplina (Banda P/M Sênior)": 3}
    problem_map = {"Seguir Regras Simples": 1, "Julgamento baseado em Prática e Experiência": 2, "Julgamento Complexo, Análise de Múltiplas Fontes (Banda P/M)": 3}
    leadership_map = {"Nenhuma responsabilidade de gestão": 1, "Orientação/Treinamento de Juniores (IC)": 2, "Responsabilidade Total de Supervisão (M1/M2)": 3}
    impact_map = {"Restrito ao próprio Time": 1, "Área/Subfunção (Ex: Contabilidade)": 2, "Função/Organização (Ex: Vice-Presidência)": 3}

    # 1. Calcula o score alvo numérico baseado nas respostas do usuário (0-12)
    target_score_num = (knowledge_map[params['knowledge_level']] + problem_map[params['problem_level']] + leadership_map[params['leadership_scope']] + impact_map[params['impact_scope']])
    
    # 2. Infere o GG Alvo (Proxy: Mapeia 0-12 para a faixa de GG mais relevante, ex: 8-17)
    # Exemplo simples: 12/12 * 9 (range max) + 8 (range min) = GG 17. 
    inferred_gg = 8 + (target_score_num / 12) * 9 
    
    # 3. Score de Proximidade (Inverso da Distância) - Core do Score (Proximidade ao GG Inferido)
    df_filtered['target_gg_normalized'] = inferred_gg / 25
    df_filtered['gg_normalized'] = df_filtered['global_grade_num'] / 25
    
    df_filtered['score_proximity'] = np.exp(-((df_filtered['gg_normalized'] - df_filtered['target_gg_normalized'])**2) / 0.05)
    df_filtered['score_proximity'] = df_filtered['score_proximity'] * weights['knowledge_level']
    
    # 4. Ajuste por Liderança (Management/IC Match) - Ponderação Final
    df_filtered['score_leadership_adjust'] = 1
    if not params['is_manager']:
        # Penaliza cargos de gestão se o usuário selecionou IC
        df_filtered.loc[df_filtered['career_path'].str.contains('manager|coordenador|supervisor', case=False, na=False), 'score_leadership_adjust'] = 0.5
    
    df_filtered['score_total'] = df_filtered['score_proximity'] * df_filtered['score_leadership_adjust']
    df_filtered['similarity'] = df_filtered['score_total']

    # Normaliza a pontuação final para 0-100%
    df_filtered['similarity'] = np.clip(df_filtered['similarity'] / df_filtered['similarity'].max() if df_filtered['similarity'].max() > 0 else 0, 0, 1)

    return df_filtered.sort_values("similarity", ascending=False)


# ===========================================================
# 5. CAMPOS DE ENTRADA DO FORMULÁRIO GGS ESTRUTURADO
# ===========================================================
st.markdown("### 🧠 Contexto Funcional e Hierarquia")

c1, c2, c3 = st.columns(3)
with c1:
    families = sorted(df["job_family"].unique())
    selected_family = st.selectbox("📂 Família (Função) *", ["Selecione..."] + families)
with c2:
    subfamilies = sorted(df[df["job_family"] == selected_family]["sub_job_family"].unique()) if selected_family != "Selecione..." else []
    selected_subfamily = st.selectbox("📂 Subfamília (Disciplina) *", ["Selecione..."] + subfamilies)
with c3:
    # REQUISITO WTW RÍGIDO: Cargo ao qual reporta (Filtro Hierárquico)
    superior = st.selectbox("📋 Cargo ao qual reporta (Filtro Rígido) *", [
        "Selecione...", "Supervisor", "Coordenador", "Gerente", "Diretor", "Vice-presidente", "Presidente / CEO"
    ])
    
st.markdown("---")
st.markdown("#### Fatores de Graduação (Simulando a Avaliação de Complexidade)")

col1, col2 = st.columns(2)

with col1:
    # Fator 1: Conhecimento Funcional 
    knowledge_level = st.selectbox(
        "1. Profundidade do Conhecimento Funcional",
        ["Rotinas/Procedimentos Definidos (Banda U/W)", 
         "Conhecimento de Conceitos e Princípios (Banda P/T)", 
         "Domínio Amplo e Integrado da Disciplina (Banda P/M Sênior)"]
    )
    
    # Fator 2: Solução de Problemas / Julgamento
    problem_level = st.selectbox(
        "2. Complexidade na Solução de Problemas",
        ["Seguir Regras Simples", 
         "Julgamento baseado em Prática e Experiência",
         "Julgamento Complexo, Análise de Múltiplas Fontes (Banda P/M)"]
    )
    
    # Fator 3: Tipo de Contribuição (IC vs. Gestor)
    is_manager_input = st.radio("3. Possui Responsabilidade de Gestão?", ["Não (IC)", "Sim (Gestor de Pessoas)"])
    is_manager = is_manager_input == "Sim (Gestor de Pessoas)"


with col2:
    # Fator 4: Escopo de Liderança (Se não for Gestor, pontua orientação/influência)
    leadership_scope = st.selectbox(
        "4. Escopo de Liderança (Apoio/Influência)",
        ["Nenhuma responsabilidade de gestão", 
         "Orientação/Treinamento de Juniores (IC)",
         "Responsabilidade Total de Supervisão (M1/M2)"]
    )

    # Fator 5: Amplitude do Impacto Organizacional
    impact_scope = st.selectbox(
        "5. Área de Impacto",
        ["Restrito ao próprio Time",
         "Área/Subfunção (Ex: Contabilidade)",
         "Função/Organização (Ex: Vice-Presidência)"]
    )
    
    # Fator Auxiliar: proxy para qualificação, como no Guia GGS
    st.caption("Fator Auxiliar: Nível Educacional")
    education_req = st.selectbox("🎓 Qualificação Mínima", ["Não especificado", "Técnico", "Superior Completo"])
    

# ===========================================================
# 6. EXECUÇÃO DE ANÁLISE (FILTRAGEM E MATCHING ESTRUTURADO)
# ===========================================================

if st.button("🔍 Analisar Aderência", type="primary", use_container_width=True):

    # 6.1. Validação de Inputs Essenciais
    required_inputs = [selected_family, selected_subfamily, superior]
    if "Selecione..." in required_inputs:
        st.warning("⚠️ Os campos Família, Subfamília e Cargo de Reporte são obrigatórios.")
        st.stop()
        
    # 6.2. Determinar o GG Máximo Permitido (Filtro Rígido Hierárquico)
    max_gg_allowed = GG_LIMITS_MAP.get(superior, 99) 
    
    # CORREÇÃO CRÍTICA DO BUG DE LEITURA: Força o limite para 12 se for Coordenador/Supervisor, ignorando o 99.
    if superior in ["Coordenador", "Supervisor"] and max_gg_allowed == 99:
        max_gg_allowed = 12 # Limite correto para Coordenador/Supervisor (GG < 12)
        
    # 6.3. Coleta de Parâmetros de Match
    match_params = {
        'knowledge_level': knowledge_level,
        'problem_level': problem_level,
        'leadership_scope': leadership_scope,
        'impact_scope': impact_scope,
        'is_manager': is_manager,
        'education': education_req
    }

    # 6.4. Aplicação do Filtro Rígido (Arquitetura e Hierarquia)
    mask = (df["job_family"] == selected_family) & \
           (df["sub_job_family"] == selected_subfamily) & \
           (df["global_grade_num"] < max_gg_allowed)
    
    filtered_df = df[mask].copy()

    if filtered_df.empty:
        st.error(f"Nenhum cargo encontrado que satisfaça os filtros de Arquitetura ({selected_family}/{selected_subfamily}) e Hierarquia (GG < {max_gg_allowed}).")
        st.stop()
    
    # 6.5. Cálculo da Pontuação de Aderência (Match Estruturado)
    results_df = calculate_structured_match(filtered_df, match_params)
    
    # 6.6. Exibição dos Top 3 Resultados
    top3 = results_df.head(3)

    # --- Guardrail de Coerência Simples ---
    if top3.empty or top3.iloc[0]["similarity"] < JOB_RULES.get("thresholds", {}).get("weak_match", 0.50):
        best_score = top3.iloc[0]["similarity"] if not top3.empty else 0.0
        threshold_weak = JOB_RULES.get("thresholds", {}).get("weak_match", 0.50)
        score_to_display = float(best_score * 100)
        
        st.markdown(f"""
        <div class="custom-error-box">
            <div class="custom-error-title">❌ Alerta: Coerência de Fatores Baixa</div>
            A pontuação do melhor cargo compatível ({score_to_display:.1f}%) está abaixo do limite de Match Fraco ({threshold_weak*100:.0f}%).
            <br>
            **Ação Necessária:** Ajuste os Fatores de Graduação (GGS) para refletir um nível de complexidade maior ou menor, que encontre aderência na sua base de dados.
        </div>
        """, unsafe_allow_html=True)
        st.stop()
        
    # --- Inferência do GG Mais Provável (Para Insight) ---
    inferred_gg_for_display = results_df.iloc[0]["global_grade"]
    
    # --- Insight Box (Adaptação para o novo modelo) ---
    st.markdown(f"""
    <div class="ai-insight-box">
        <div class="ai-insight-title">📊 Análise de Aderência Estruturada (GGS)</div>
        **Filtros Rígidos:** Família, Disciplina e Hierarquia (GG < **{max_gg_allowed}**).<br>
        **Global Grade Mais Provável (GG):** **{inferred_gg_for_display}** (Este é o resultado do match de maior pontuação).<br>
        **Aderência:** Ranqueado pela proximidade das suas respostas aos Fatores de Graduação (GGS).
    </div>
    """, unsafe_allow_html=True)


    # ===========================================================
    # 7. GRID FINAL (EXIBIÇÃO DOS CARGOS)
    # ===========================================================
    
    st.markdown("---")
    st.header("🏆 Cargos Mais Compatíveis")

    cards_data = []
    
    for _, row in top3.iterrows():
        lvl_name = ""
        gg_val = str(row["global_grade"]).strip() 
        
        if not df_levels.empty and "global_grade" in df_levels.columns and "level_name" in df_levels.columns:
            match = df_levels[df_levels["global_grade"].astype(str).str.strip() == gg_val]
            if not match.empty:
                lvl_name = f"• {match['level_name'].iloc[0]}"
        cards_data.append({
            "row": row,
            "score_fmt": f"{row['similarity']*100:.1f}%",
            "score_bg": "#145efc",
            "lvl": lvl_name
        })

    num_results = len(cards_data)
    grid_style = f"grid-template-columns: repeat({num_results}, 1fr);"
    grid_html = f'<div class="comparison-grid" style="{grid_style}">'

    # Lógica de renderização completa do grid (simplificada para o contexto)
    sections_config = [
        ("🧭 Sub Job Family Description", "sub_job_family_description", "#95a5a6"),
        ("🧠 Job Profile Description", "job_profile_description", "#e91e63"),
        ("🏛️ Career Band Description", "career_band_description", "#673ab7"),
    ]

    # 1. Cabeçalho
    for card in cards_data:
        d = card['row']
        grid_html += f"""
        <div class="grid-cell header-cell">
            <div class="fjc-title">{html.escape(d.get('job_profile', '-'))}</div>
            <div class="fjc-gg-row">
                <div class="fjc-gg">GG {d.get('global_grade', '-')} {card['lvl']}</div>
                <div class="fjc-score">{card['score_fmt']} Match</div>
            </div>
        </div>
        <div class="grid-cell meta-cell">
            <div class="meta-row"><strong>Família:</strong> {html.escape(d.get('job_family', '-'))}</div>
            <div class="meta-row"><strong>Subfamília:</strong> {html.escape(d.get('sub_job_family', '-'))}</div>
            <div class="meta-row"><strong>Carreira:</strong> {html.escape(d.get('career_path', '-'))}</div>
        </div>
        """

    # 2. Seções de Conteúdo (Exibindo 3 das seções de descrição)
    for title, field, color in sections_config:
        for card in cards_data:
            content = str(card['row'].get(field, '')).strip()
            if content.lower() in ('nan', '-'):
                content = ''
            
            grid_html += f"""
            <div class="grid-cell section-cell" style="border-left-color: {color};">
                <div class="section-title" style="color: {color};">{title}</div>
                <div class="section-content">{html.escape(content)}</div>
            </div>"""
    
    # 3. Rodapé
    for _ in cards_data:
        grid_html += '<div class="grid-cell footer-cell"></div>'

    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)
