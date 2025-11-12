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
    # Caminho ajustado para a pasta 'job_architecture/data' se for o caso real
    # Por enquanto, assumindo que está na mesma estrutura dos arquivos fornecidos
    path = Path("job_rules.json") 
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"thresholds": {"weak_match": 0.50}} # Default fallback

@st.cache_data
def load_data():
    """Carrega os dados, aplica a sanitização e cria a coluna Global Grade Num."""
    data = load_excel_data()
    
    df_jobs = sanitize_columns(data.get("job_profile", pd.DataFrame())).fillna("")
    df_levels = sanitize_columns(data.get("level_structure", pd.DataFrame())).fillna("")
    
    if "global_grade" in df_jobs.columns:
        # Garante que o GG seja numérico para o filtro hierárquico
        df_jobs["global_grade_num"] = pd.to_numeric(df_jobs["global_grade"], errors="coerce").fillna(0).astype(int)
    else:
        # Adiciona coluna de fallback se não existir
        df_jobs["global_grade_num"] = 0 
    
    return df_jobs, df_levels

df, df_levels = load_data()
model = load_model()
JOB_RULES = load_json_rules()

# Mapeamento do GG Máximo do subordinado com base no Cargo Superior (Regra WTW Rígida)
# O GG Máximo aqui é o TETO permitido, ou seja, cargo_candidato.GG < GG_LIMITS_MAP[superior]
# Esses valores são baseados na sobreposição de GGs entre níveis (EX/M3/M2/M1/P4/P3/P2)
GG_LIMITS_MAP = {
    # Nível Executive/CEO
    "Presidente / CEO": 24, # Subordinado Max: GG 23 (VP/Diretor Sênior)
    "Vice-presidente": 21,   # Subordinado Max: GG 20 (Diretor)
    "Diretor": 18,           # Subordinado Max: GG 17 (Gerente Sênior M3/M4)
    
    # Nível Management
    "Gerente": 15,           # Subordinado Max: GG 14 (Coordenador/Especialista M1/P4)
    
    # Nível Supervisory / Expert
    "Coordenador": 12,       # Subordinado Max: GG 11 (Analista Pleno/Sênior P2/P3)
    "Supervisor": 12         # Subordinado Max: GG 11 (Analista Pleno/Sênior P2/P3)
}

# Mapeamento de GGs por Career Level (Para sugestão otimizada)
LEVEL_GG_MAPPING = {
    "W1":list(range(1, 6)), "W2":list(range(5, 9)), "W3":list(range(7, 11)),
    "P1":list(range(8, 11)), "P2":list(range(10, 13)), "P3":list(range(12, 15)), "P4":list(range(14, 18)),
    "M1":list(range(11, 15)), "M2":list(range(14, 17)), "M3":list(range(16, 20)),
    "E1":list(range(18, 22)), "E2":list(range(21, 26))
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
# Obtém todas as famílias e subfamílias únicas dos dados
all_families = sorted(df["job_family"].unique())
with c1:
    selected_family = st.selectbox("📂 Família (Obrigatório)", ["Selecione..."] + all_families)
with c2:
    if selected_family != "Selecione...":
        subfamilies = sorted(df[df["job_family"] == selected_family]["sub_job_family"].unique())
    else:
        subfamilies = []
    selected_subfamily = st.selectbox("📂 Subfamília (Obrigatório)", ["Selecione..."] + subfamilies)

desc_input = st.text_area("📝 Descrição detalhada do cargo (mínimo 50 palavras):", height=200)
word_count = len(desc_input.strip().split())
st.caption(f"Contagem de palavras: {word_count} / 50")

# ===========================================================
# 6. DETECÇÃO DE NÍVEL E MATCHING (BASEADO EM WTW/GGS)
# ===========================================================

def infer_market_level(superior, lidera, abrangencia):
    """
    Infernir o nível de carreira WTW (W, P, M, E) baseado em regras hierárquicas e escopo.
    Esta função é conservadora e o filtro hierárquico rígido (GG_LIMITS_MAP) prevalece.
    """
    
    # 1. Baseado na Hierarquia (Topo da Carreira)
    if superior in ["Presidente / CEO"]:
        return "E1" # Diretor ou VP
    if superior in ["Vice-presidente", "Diretor"]:
        return "M3" # Gerente Sênior / Head (M3)
        
    # 2. Baseado na Abrangência/Escopo
    if abrangencia in ["Global", "Multipaís"]:
        # Se reporta a Gerente/Coordenador, mas tem escopo Global/Multipaís, 
        # sugere um Especialista Sênior (P4) ou M1 (Coordenador)
        if lidera == "Sim":
            return "M1"
        return "P4" 
        
    # 3. Baseado em Liderança e Subordinação
    if superior == "Gerente":
        if lidera == "Sim":
            return "M1" # Supervisor/Coordenador
        return "P3" # Analista Sênior / Especialista
        
    if superior in ["Coordenador", "Supervisor"]:
        if lidera == "Sim":
             return "W3" # Líder de Produção/Operacional
        return "P2" # Analista Pleno / Analista Júnior

    return "W2" # Nível Operacional Padrão (W2)

# ===========================================================
# 7. EXECUÇÃO DE ANÁLISE (FILTRAGEM HIERÁRQUICA E OTIMIZAÇÃO DO MATCHING)
# ===========================================================
if st.button("🔍 Analisar Aderência", type="primary", use_container_width=True):

    # 7.1. Validação de Inputs
    required_inputs = [superior, lidera, abrangencia, selected_family, selected_subfamily]
    if "Selecione..." in required_inputs or word_count < 50:
        st.warning("⚠️ Todos os campos obrigatórios devem ser preenchidos e a descrição deve ter no mínimo 50 palavras.")
        st.stop()

    detected_key = infer_market_level(superior, lidera, abrangencia)
    
    # 7.2. Obter o GG Máximo Permitido (Regra RÍGIDA WTW: Subordinado < Superior)
    max_gg_allowed = GG_LIMITS_MAP.get(superior, 99) 
    
    # Obter os GGs sugeridos pela Banda WTW
    allowed_grades_wtw = LEVEL_GG_MAPPING.get(detected_key, [])

    st.markdown(f"""
    <div class="ai-insight-box">
        <div class="ai-insight-title">🤖 Contexto Hierárquico Detectado (Guia WTW)</div>
        <strong>Banda de Carreira Sugerida:</strong> {detected_key} (GGs {min(allowed_grades_wtw)}-{max(allowed_grades_wtw)}).<br>
        <strong>Filtro Hierárquico Rígido:</strong> O cargo pesquisado deve ter um **Global Grade estritamente menor** que **{max_gg_allowed}** (GG < {max_gg_allowed}) para respeitar a hierarquia.
    </div>
    """, unsafe_allow_html=True)

    # 7.3. Aplicação dos Filtros WTW
    # 1. Filtro de Arquitetura (Família/Subfamília)
    mask = (df["job_family"] == selected_family) & (df["sub_job_family"] == selected_subfamily)
    
    # 2. Filtro Hierárquico RÍGIDO: Garante que o GG do cargo pesquisado seja estritamente inferior ao limite do superior.
    mask &= (df["global_grade_num"] < max_gg_allowed)
    
    # 3. Filtro Otimizado de Banda WTW: Refina o resultado para a banda de carreira sugerida.
    if allowed_grades_wtw:
        mask &= df["global_grade_num"].isin(allowed_grades_wtw) 
        
    
    filtered = df[mask].copy()

    if filtered.empty:
        st.error(f"""
        ❌ **Nenhum Cargo Compatível Encontrado.** <br>
        O filtro combinado de **Arquitetura (Família/Subfamília)** e **Hierarquia (GG < {max_gg_allowed})** não retornou nenhum resultado. 
        <br>
        Isso pode ocorrer se não houverem cargos de nível {detected_key} (GG < {max_gg_allowed}) registrados nesta Família/Subfamília no seu arquivo de dados. 
        <br>
        Tente ajustar o **Cargo ao qual reporta** ou a **Família/Subfamília**.
        """, unsafe_allow_html=True)
        st.stop()
    
    # 7.4. Cálculo de Similaridade (Precisão Semântica)
    # Incluindo múltiplos campos para aumentar a precisão do match de conteúdo (Guia WTW: Job Content)
    job_texts = (
        filtered["job_profile"].fillna("") + ". " +
        filtered["role_description"].fillna("") + ". " +
        filtered["qualifications"].fillna("") + ". " +
        filtered["specific_parameters_kpis"].fillna("") + ". " +
        filtered["competencies_1"].fillna("") + ". " +
        filtered["competencies_2"].fillna("") + ". " +
        filtered["competencies_3"].fillna("")
    ).tolist()
    
    query_emb = model.encode([desc_input], show_progress_bar=False)[0]
    job_emb = model.encode(job_texts, show_progress_bar=False)
    sims_sem = cosine_similarity([query_emb], job_emb)[0]

    tfidf = TfidfVectorizer(max_features=10000, ngram_range=(1,2)).fit(job_texts)
    job_tfidf = tfidf.transform(job_texts)
    query_tfidf = tfidf.transform([desc_input])
    sims_kw = cosine_similarity(query_tfidf, job_tfidf)[0]

    # Ponderação Final (75% Semântica, 25% Keyword)
    sims = 0.75 * sims_sem + 0.25 * sims_kw
    filtered["similarity"] = sims
    top3 = filtered.sort_values("similarity", ascending=False).head(3)
    
    best_score = top3.iloc[0]["similarity"] if not top3.empty else 0.0
    threshold_weak = JOB_RULES.get("thresholds", {}).get("weak_match", 0.50)

    # 7.5. Guardrail de Coerência (Verificação de Incoerência Semântica)
    if best_score < threshold_weak:
        st.error(f"""
        ❌ **Alerta: Incoerência de Conteúdo (Baixa Aderência)**
        <br>
        A pontuação do melhor cargo compatível ({best_score*100:.1f}%) está abaixo do limite de Match Fraco ({threshold_weak*100:.0f}%).
        <br>
        Isso indica que a sua **Descrição Detalhada do Cargo** não é semanticamente coerente com o conteúdo dos cargos já existentes na **Família/Subfamília ({selected_family}/{selected_subfamily})**. 
        <br>
        **Ação Necessária:** Por favor, **refine o texto da descrição** para que ele reflita melhor o conteúdo dos cargos dessa área, ou verifique se a **Família/Subfamília** selecionada está correta.
        """, unsafe_allow_html=True)
        st.stop()


    # ===========================================================
    # 8. GRID FINAL (EXIBIÇÃO)
    # ===========================================================
    st.markdown("---")
    st.header("🏆 Cargos Mais Compatíveis")

    cards_data = []
    for _, row in top3.iterrows():
        score_val = float(row["similarity"]) * 100
        score_bg = "#145efc"
        lvl_name = ""
        gg_val = str(row["global_grade"]).strip() 
        
        # Mapeia o Global Grade para o Level Name (Ex: P4, M2)
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
