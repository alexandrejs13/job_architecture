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
    # Carrega o NOVO JSON UNIFICADO
    path = Path("wtw_match_rules.json") # Assumindo este é o nome do arquivo unificado
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"thresholds": {"weak_match": 0.50}, "career_bands": {}, "wtw_reporting_limits": {}, "level_keywords": {}} # Default fallback

@st.cache_data
def load_data():
    """Carrega os dados, aplica a sanitização e cria a coluna Global Grade Num."""
    # Nota: load_excel_data() deve ser fornecido
    # Assumindo que o load_excel_data() carrega os dados corretamente
    # Para fins de demonstração, simulamos um DataFrame vazio
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

# EXTRAÇÃO DAS REGRAS WTW DO NOVO JSON UNIFICADO
GG_LIMITS_MAP = JOB_RULES.get("wtw_reporting_limits", {})

LEVEL_GG_MAPPING = {}
for band, data in JOB_RULES.get("career_bands", {}).items():
    if data and "gg_range" in data and len(data["gg_range"]) == 2:
        start, end = data["gg_range"]
        LEVEL_GG_MAPPING[band] = list(range(start, end + 1))
        
LEVEL_KEYWORDS = JOB_RULES.get("level_keywords", {})


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

def ggs_decision_score(desc_text, superior_reporta, lidera_equipe, abrangencia_funcao):
    """
    Pontua a descrição do cargo e as entradas de escopo para simular a Árvore de Decisão GGS (Pág. 44).
    Retorna a Banda GGS (1, 2, 3IC, 4IC, 3M, 4M, 5FS, 5BS, 6) mais provável.
    """
    desc_lower = desc_text.lower()
    
    # --- Passo 1: Gerencia Pessoas? (Managing people a focus?) [cite: 581, 838] ---
    # Usamos o input 'lidera' e reforçamos com keywords (Gestão de projetos/equipes/vendors de longo prazo).
    is_management_focus = lidera_equipe == "Sim"
    if not is_management_focus:
        # Reforça IC: verifica palavras-chave de gestão indireta/foco em expertise.
        management_kws = LEVEL_KEYWORDS.get("M", []) + LEVEL_KEYWORDS.get("EX", [])
        ic_kws = LEVEL_KEYWORDS.get("P", []) + LEVEL_KEYWORDS.get("U", []) + LEVEL_KEYWORDS.get("W", [])
        
        m_score = sum(1 for kw in management_kws if kw in desc_lower)
        ic_score = sum(1 for kw in ic_kws if kw in desc_lower)
        
        # Se a descrição tem forte indicação de gestão (ex: "coordena", "supervisiona") ou estratégia, 
        # considera foco em gestão, mesmo sem time direto (dotted-line reports)[cite: 586].
        if m_score > ic_score and m_score > 3:
            is_management_focus = True

    # --- SIM: Carreira de Management (3M, 4M, 5FS, 5BS, 6) ---
    if is_management_focus:
        # 1. CEO/Business Unit Manager? (Banda 6) [cite: 672, 858, 864]
        if superior_reporta in ["Presidente / CEO", "Vice-presidente"]:
             # Se o cargo reporta ao CEO ou VP (o topo da hierarquia), ele é EX (Banda 6) se for C-Level/Head of Function.
             # Como o GG LIMITS já filtra o GG, definimos como 6 (a banda EX/Top Management mais provável).
            return "6" 
            
        # 2. Set/Significantly influence business strategy? (5FS ou 5BS) [cite: 650, 851]
        # Se reporta a Diretor/VP (i.e., é Head de Função)
        if superior_reporta in ["Diretor", "Vice-presidente"] or "estratégia de negócio" in desc_lower or "define a visão" in desc_lower:
            # Em organizações maiores (CEO Grade 19+), distingue 5FS e 5BS. Aqui, usamos a abrangência como proxy para Business Strategy.
            if abrangencia in ["Global", "Multipaís"]:
                return "5BS" # Business Strategy (Maior escopo/impacto estratégico) [cite: 579, 653]
            return "5FS" # Functional Strategy (Função chave com grande impacto) [cite: 578, 630]
            
        # 3. Set/Significantly influence functional strategy? (4M ou 3M) [cite: 630, 843]
        if superior_reporta in ["Gerente"] or "estratégia funcional" in desc_lower or "define políticas operacionais" in desc_lower:
            # Média e Alta Gerência
            if "multiplas áreas" in desc_lower or "mais de 10 subordinados" in desc_lower:
                return "4M" # Middle Management (Múltiplos times/Sub-funções) [cite: 621, 1997]
            return "3M" # Junior Management/Supervisor (Primeira linha de gerência) [cite: 629, 1644]
            
        # Se não se enquadrou acima, é um Supervisor de base ou IC que foi puxado por keywords
        return "3M"

    # --- NÃO: Carreira de Individual Contributor (1, 2, 3IC, 4IC) ---
    else:
        # 1. Specific job functional knowledge? (NÃO é Banda 1) [cite: 694, 842]
        # Banda 1 (Manual/Junior Admin) - Não exige conhecimento funcional ou treinamento prévio. [cite: 700, 876]
        if not ("conhecimento" in desc_lower or "técnico" in desc_lower or "educação formal" in desc_lower or any(kw in desc_lower for kw in LEVEL_KEYWORDS.get("W", []))):
             return "1" 

        # 2. Independence in applying professional expertise? (3IC, 4IC vs Banda 2) [cite: 718, 849]
        # Profissionais (3IC/4IC) vs Clerical/Admin/Technical (Banda 2)
        if "independente" in desc_lower or "julgamento" in desc_lower or "expertise profissional" in desc_lower or "resolver problemas" in desc_lower:
            
            # 3. Subject Matter Expert (SME)? (Banda 4IC vs 3IC) [cite: 746, 856]
            if "expert" in desc_lower or "líder técnico" in desc_lower or "autoridade reconhecida" in desc_lower or "guru" in desc_lower or "poucos pares técnicos" in desc_lower:
                return "4IC" # Subject Matter Expert [cite: 749, 3699]
            
            # Se não é SME, é Professional (3IC)
            return "3IC" # Professional (Aplica expertise e julgamento de forma independente) [cite: 701, 3701]
        
        # Se não há independência, é Banda 2 (Clerical/Admin/Técnico) [cite: 725, 3703]
        return "2" 


def infer_market_band(superior, lidera, abrangencia, desc_input):
    # Wrapper para simular a Árvore de Decisão
    # Para o propósito desta função, mapeamos as bandas GGS para as bandas WTW (M, P, W, EX) se necessário.
    
    ggs_band = ggs_decision_score(desc_input, superior, lidera, abrangencia)
    
    # Mapeamento para as bandas WTW usadas nos GGs (EX: 5BS, 5FS, 6 -> EX/M; 3IC, 4IC -> P; 1, 2 -> W/U)
    if ggs_band in ["6", "5BS", "5FS"]:
        return "EX"
    elif ggs_band in ["4M", "3M"]:
        return "M"
    elif ggs_band in ["4IC", "3IC"]:
        return "P"
    elif ggs_band in ["2"]:
        # Banda 2 abrange Technical (T) e Clerical/Admin (U), que na estrutura simples são U.
        return "U" 
    elif ggs_band in ["1"]:
        return "W" # Manual/Junior Admin
        
    return "P" # Default fallback


# ===========================================================
# 7. EXECUÇÃO DE ANÁLISE (FILTRAGEM HIERÁRQUICA E OTIMIZAÇÃO DO MATCHING)
# ===========================================================
if st.button("🔍 Analisar Aderência", type="primary", use_container_width=True):

    # 7.1. Validação de Inputs
    required_inputs = [superior, lidera, abrangencia, selected_family, selected_subfamily]
    if "Selecione..." in required_inputs or word_count < 50:
        st.warning("⚠️ Todos os campos obrigatórios devem ser preenchidos e a descrição deve ter no mínimo 50 palavras.")
        st.stop()
        
    # Chama a função revisada que considera a descrição E as regras GGS
    detected_band = infer_market_band(superior, lidera, abrangencia, desc_input)
    
    # 7.2. Obter o GG Máximo Permitido (Regra RÍGIDA WTW: Subordinado < Superior)
    max_gg_allowed = GG_LIMITS_MAP.get(superior, 99) 
    
    # Obtemos a faixa de GGs sugeridos pela Banda detectada
    allowed_grades_wtw = LEVEL_GG_MAPPING.get(detected_band, [])
    
    # Aplicamos o filtro rígido de hierarquia na faixa sugerida
    if allowed_grades_wtw:
        allowed_grades_wtw = [gg for gg in allowed_grades_wtw if gg < max_gg_allowed]
        if not allowed_grades_wtw:
            st.error(f"""
            ❌ **Conflito de Nível Hierárquico (Regra WTW Rígida).**
            <br>
            A banda de carreira sugerida (**{detected_band}**) ou a Descrição do Cargo sugere um nível que não respeita o **Filtro Hierárquico Rígido** (GG < {max_gg_allowed}).
            <br>
            Ajuste o **Cargo ao qual reporta** ou refine a **Descrição Detalhada do Cargo** para um nível mais operacional/júnior.
            """, unsafe_allow_html=True)
            st.stop()

    min_gg_suggested = min(allowed_grades_wtw) if allowed_grades_wtw else 0
    max_gg_suggested = max(allowed_grades_wtw) if allowed_grades_wtw else max_gg_allowed - 1
    
    st.markdown(f"""
    <div class="ai-insight-box">
        <div class="ai-insight-title">🤖 Contexto Hierárquico e de Conteúdo Detectado (GGS 4.2)</div>
        **Banda de Carreira Sugerida:** **{detected_band}** (GGs Válidos: **{min_gg_suggested}** a **{max_gg_suggested}**).<br>
        **Filtro Hierárquico Rígido:** O cargo deve ter um **Global Grade estritamente menor** que **{max_gg_allowed}** (GG < {max_gg_allowed}).
    </div>
    """, unsafe_allow_html=True)

    # 7.3. Aplicação dos Filtros GGS
    
    # 1. Filtro de Arquitetura (Família/Subfamília)
    mask = (df["job_family"] == selected_family) & (df["sub_job_family"] == selected_subfamily)
    
    # 2. Filtro Hierárquico RÍGIDO E OTIMIZADO
    if allowed_grades_wtw:
        mask &= df["global_grade_num"].isin(allowed_grades_wtw) 
        
    
    filtered = df[mask].copy()

    if filtered.empty:
        st.error(f"""
        ❌ **Nenhum Cargo Compatível Encontrado.** <br>
        O filtro combinado de **Arquitetura (Família/Subfamília)** e **Hierarquia (GG < {max_gg_allowed})** não retornou nenhum resultado no range **{min_gg_suggested}** a **{max_gg_suggested}**. 
        <br>
        Verifique se existem cargos no seu arquivo de dados que atendam a todos os critérios.
        """, unsafe_allow_html=True)
        st.stop()
    
    # 7.4. Cálculo de Similaridade (Precisão Semântica - 7 Fatores de Graduação)
    # A precisão é determinada comparando a descrição do usuário (que deve refletir os 7 fatores) com o conteúdo dos jobs.
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
        **Ação Necessária:** Por favor, **refine o texto da descrição** para que ele reflita melhor o conteúdo dos cargos dessa área, usando termos que remetam aos **7 Fatores de Graduação (GGS)**.
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
