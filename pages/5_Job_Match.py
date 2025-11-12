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

# ===========================================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ===========================================================
st.set_page_config(
    page_title="Job Match",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================================================
# 2. CSS GLOBAL (MESMO PADRÃO DA PÁGINA JOB PROFILE DESCRIPTION)
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
</style>

<div class="page-header">
  <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/checkmark%20success.png" alt="icon">
  Análise de Aderência de Cargo (Job Match)
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
    path = Path("job_architecture/data/job_rules.json")
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

@st.cache_data
def load_data():
    """Carrega os dados, aplica a sanitização e cria a coluna Global Grade Num."""
    data = load_excel_data()
    
    df_jobs = sanitize_columns(data.get("job_profile", pd.DataFrame())).fillna("")
    df_levels = sanitize_columns(data.get("level_structure", pd.DataFrame())).fillna("")
    
    if "global_grade" in df_jobs.columns:
        df_jobs["global_grade_num"] = pd.to_numeric(df_jobs["global_grade"], errors="coerce").fillna(0).astype(int)
    
    return df_jobs, df_levels

df, df_levels = load_data()
model = load_model()
JOB_RULES = load_json_rules()

# Mapeamento do GG Máximo do subordinado com base no Cargo Superior
# O GG Máximo aqui representa o TETO que o CARGO PESQUISADO pode ter.
GG_LIMITS_MAP = {
    # Se o superior é Supervisor/Coordenador (GG 11-14), o subordinado deve ser Analista Pleno/Senior (GG 10-12)
    "Supervisor": 12, # GG Máximo do subordinado deve ser GG 11 (Analista Pleno/Sênior P2/P3)
    "Coordenador": 12, # GG Máximo do subordinado deve ser GG 11 (Analista Pleno/Sênior P2/P3)
    
    # Se o superior é Gerente (GG 14-16), o subordinado pode ser Coordenador (GG 11-14)
    "Gerente": 14, 
    
    # Se o superior é Diretor (GG 18-21), o subordinado pode ser Gerente (GG 14-16)
    "Diretor": 17, 
    
    # Níveis Executivos
    "Vice-presidente": 20, 
    "Presidente / CEO": 23 
}

# ===========================================================
# 4. CAMPOS DE ENTRADA (WTW)
# ===========================================================
st.markdown("### 🔧 Parâmetros Hierárquicos e Organizacionais")

c1, c2, c3 = st.columns(3)
with c1:
    superior = st.selectbox("📋 Cargo ao qual reporta *", [
        "Selecione...", "Supervisor", "Coordenador", "Gerente", "Diretor", "Vice-presidente", "Presidente / CEO"
    ])
with c2:
    lidera = st.selectbox("👥 Possui equipe? *", ["Selecione...", "Sim", "Não"])
with c3:
    abrangencia = st.selectbox("🌍 Abrangência da função *", [
        "Selecione...", "Local", "Regional (mais de 1 estado)", "Nacional", "Multipaís", "Global"
    ])

if lidera == "Sim":
    c4, c5 = st.columns(2)
    with c4:
        subordinados = st.selectbox("📈 Nº de subordinados diretos *", [
            "0-5", "6-10", "11-20", "21-50", "51-100", "100+"
        ])
    with c5:
        multiplas_areas = st.selectbox("🏢 Responsável por múltiplas áreas / funções? *", ["Não", "Sim"])
else:
    subordinados = "0"
    multiplas_areas = "Não"

st.divider()

# ===========================================================
# 5. CONTEXTO FUNCIONAL E DESCRIÇÃO
# ===========================================================
st.markdown("### 🧠 Contexto Funcional e Descrição do Cargo")

c1, c2 = st.columns(2)
with c1:
    families = sorted(df["job_family"].unique())
    selected_family = st.selectbox("📂 Família (Obrigatório)", ["Selecione..."] + families)
with c2:
    subfamilies = sorted(df[df["job_family"] == selected_family]["sub_job_family"].unique()) if selected_family != "Selecione..." else []
    selected_subfamily = st.selectbox("📂 Subfamília (Obrigatório)", ["Selecione..."] + subfamilies)

desc_input = st.text_area("📝 Descrição detalhada do cargo (mínimo 50 palavras):", height=200)
word_count = len(desc_input.strip().split())
st.caption(f"Contagem de palavras: {word_count} / 50")

# ===========================================================
# 6. DETECÇÃO DE NÍVEL E MATCHING
# ===========================================================
LEVEL_GG_MAPPING = {
    "W1":[1,2,3,4,5],"W2":[5,6,7,8],"W3":[7,8,9,10],
    "P1":[8,9,10],"P2":[10,11,12],"P3":[12,13,14],"P4":[14,15,16,17],
    "M1":[11,12,13,14],"M2":[14,15,16],"M3":[16,17,18,19],
    "E1":[18,19,20,21],"E2":[21,22,23,24,25]
}

def infer_market_level(superior, lidera, subordinados, abrangencia):
    # Lógica ajustada para ser mais conservadora e sugerir o nível do cargo que está sendo criado
    if superior in ["Presidente / CEO", "Vice-presidente"]:
        return "E1" # Sugere Diretor
    if superior == "Diretor" or abrangencia in ["Multipaís", "Global"]:
        return "M3" # Sugere Gerente Sênior/Head
    if superior == "Gerente":
        if lidera == "Sim" and subordinados in ["6-10","11-20","21-50","51-100","100+"]:
            return "M1" # Sugere Coordenador/Supervisor (GG 11-14)
        else:
            return "P4" # Sugere Especialista (GG 14-17)
    if superior in ["Coordenador","Supervisor"]:
        # Se reporta a Coordenador, o cargo é Analista Pleno/Sênior (P2 ou P3)
        if lidera == "Sim":
             return "W3" # Sugere Líder de Produção (GG 7-10)
        return "P2" # Sugere Analista Pleno (GG 10-12)
    return "W2" # Cargo operacional se reporta a nada acima

# ===========================================================
# 7. EXECUÇÃO DE ANÁLISE (FILTRAGEM HIERÁRQUICA APLICADA)
# ===========================================================
if st.button("🔍 Analisar Aderência", type="primary", use_container_width=True):

    if "Selecione..." in [superior,lidera,abrangencia,selected_family,selected_subfamily] or word_count < 50:
        st.warning("⚠️ Todos os campos obrigatórios devem ser preenchidos corretamente.")
        st.stop()

    detected_key = infer_market_level(superior,lidera,subordinados,abrangencia)
    allowed_grades = LEVEL_GG_MAPPING.get(detected_key, [])
    
    # 1. Obter o GG Máximo Permitido para o Cargo Subordinado
    max_gg_allowed = GG_LIMITS_MAP.get(superior, 99) 

    st.markdown(f"""
    <div class="ai-insight-box">
        <div class="ai-insight-title">🤖 Contexto Hierárquico Detectado</div>
        <strong>Banda sugerida (WTW):</strong> {detected_key} (GGs {allowed_grades}).<br>
        <strong>GG Máximo Permitido:</strong> O cargo pesquisado deve ter um **Global Grade estritamente menor** que {max_gg_allowed}.
    </div>
    """, unsafe_allow_html=True)

    # 2. Filtragem de Máscara (Family/Subfamily e GG Range)
    mask = (df["job_family"] == selected_family) & (df["sub_job_family"] == selected_subfamily)
    
    # Filtro 1: Filtro de Range WTW (Fortemente recomendado)
    if allowed_grades:
        mask &= df["global_grade_num"].isin(allowed_grades) 

    # Filtro 2 (CRÍTICO): FILTRAGEM HIERÁRQUICA POR GG MÁXIMO
    # O GG do cargo candidato deve ser estritamente menor que o GG limite do superior.
    mask &= (df["global_grade_num"] < max_gg_allowed)
        
    if not mask.any():
        st.error("Nenhum cargo encontrado dentro dos filtros de Família, Subfamília, Banda Sugerida e Hierarquia (GG inferior ao superior). Tente ajustar o cargo superior ou a descrição para que o GG sugerido não entre em conflito com o GG máximo do subordinado.")
        st.stop()

    filtered = df[mask].copy()
    
    # Usando nomes de colunas normalizados para o Matching (MANTIDO)
    job_texts = (filtered["job_profile"].fillna("") + ". " +
                 filtered["role_description"].fillna("") + ". " +
                 filtered["qualifications"].fillna("")).tolist()

    job_emb = model.encode(job_texts, show_progress_bar=False)
    query_emb = model.encode([desc_input], show_progress_bar=False)[0]
    sims_sem = cosine_similarity([query_emb], job_emb)[0]

    tfidf = TfidfVectorizer(max_features=10000, ngram_range=(1,2)).fit(job_texts)
    job_tfidf = tfidf.transform(job_texts)
    query_tfidf = tfidf.transform([desc_input])
    sims_kw = cosine_similarity(query_tfidf, job_tfidf)[0]

    sims = 0.75 * sims_sem + 0.25 * sims_kw
    filtered["similarity"] = sims
    top3 = filtered.sort_values("similarity", ascending=False).head(3)

    # ===========================================================
    # 8. GRID FINAL (IDÊNTICO AO JOB PROFILE DESCRIPTION)
    # ===========================================================
    st.markdown("---")
    st.header("🏆 Cargos Mais Compatíveis")

    if len(top3) < 1:
        st.warning("Nenhum resultado encontrado. Tente ajustar a descrição ou filtros.")
        st.stop()

    cards_data = []
    for _, row in top3.iterrows():
        score_val = float(row["similarity"]) * 100
        score_bg = "#145efc"
        lvl_name = ""
        gg_val = str(row["global_grade"]).strip() 
        
        if not df_levels.empty and "global_grade" in df_levels.columns and "level_name" in df_levels.columns:
            match = df_levels[df_levels["global_grade"].astype(str).str.strip() == gg_val]
            if not match.empty:
                lvl_name = f"• {match['level_name'].iloc[0]}"
        cards_data.append({
            "row": row,
            "score_fmt": f"{score_val:.1f}%",
            "score_bg": score_bg,
            "lvl": lvl_name
        })

    num_results = len(cards_data)
    grid_style = f"grid-template-columns: repeat({num_results}, 1fr);"
    grid_html = f'<div class="comparison-grid" style="{grid_style}">'

    # CONFIGURAÇÃO DAS SEÇÕES: MANTENDO A REFERÊNCIA EM SNAKE_CASE
    sections_config = [
        ("🧭 Sub Job Family Description", "sub_job_family_description", "#95a5a6"),
        ("🧠 Job Profile Description", "job_profile_description", "#e91e63"),
        ("🏛️ Career Band Description", "career_band_description", "#673ab7"),
        ("🎯 Role Description", "role_description", "#145efc"), 
        ("🏅 Grade Differentiator", "grade_differentiator", "#ff9800"),
        ("🎓 Qualifications", "qualifications", "#009688"),
        
        ("📊 Specific parameters / KPIs", "specific_parameters_kpis", "#c0392b"),
        ("💡 Competencies 1", "competencies_1", "#c0392b"),
        ("💡 Competencies 2", "competencies_2", "#c0392b"),
        ("💡 Competencies 3", "competencies_3", "#c0392b"),
    ]

    # 1. Cabeçalho
    for card in cards_data:
        grid_html += f"""
        <div class="grid-cell header-cell">
            <div class="fjc-title">{html.escape(card['row'].get('job_profile', '-'))}</div>
            <div class="fjc-gg-row">
                <div class="fjc-gg">GG {card['row'].get('global_grade', '-')} {card['lvl']}</div>
                <div class="fjc-score">{card['score_fmt']} Match</div>
            </div>
        </div>"""

    # 2. Metadados
    for card in cards_data:
        d = card['row']
        meta = []
        for lbl, col in [("Família","job_family"),("Subfamília","sub_job_family"),("Carreira","career_path"),("Cód","full_job_code")]:
            val = str(d.get(col,"") or "-").strip()
            meta.append(f'<div class="meta-row"><strong>{lbl}:</strong> {html.escape(val)}</div>')
        grid_html += f'<div class="grid-cell meta-cell">{"".join(meta)}</div>'

    # 3. Seções coloridas (FORÇANDO A RENDERIZAÇÃO DO TÍTULO, SE VAZIO)
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

    # 4. Rodapé
    for _ in cards_data:
        grid_html += '<div class="grid-cell footer-cell"></div>'

    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)
