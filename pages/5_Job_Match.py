# -*- coding: utf-8 -*-
# pages/5_🧩_Job_Match.py

import streamlit as st
import pandas as pd
import numpy as np
import html
import json
import re
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
from utils.data_loader import load_excel_data
from utils.ui_components import lock_sidebar
from utils.ui import setup_sidebar

# ===========================================================
# 1. CONFIGURAÇÃO DE PÁGINA (layout/visual inalterados)
# ===========================================================
st.set_page_config(layout="wide", page_title="🧩 Job Match", page_icon="✅")

# ===========================================================
# 2. CSS GLOBAL E SIDEBAR (inalterados)
# ===========================================================
css_path = Path(__file__).parents[1] / "assets" / "header.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

setup_sidebar()
lock_sidebar()

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
h1 { display: none !important; }
.block-container { max-width: 95% !important; padding-left: 1rem !important; padding-right: 1rem !important; }
.stTextArea textarea {font-size: 16px !important;}
.comparison-grid { display: grid; gap: 20px; margin-top: 20px; }
.grid-cell { background: #fff; border: 1px solid #e0e0e0; padding: 15px; display: flex; flex-direction: column; }
.header-cell { background: #f8f9fa; border-radius: 12px 12px 0 0; border-bottom: none; }
.fjc-title { font-size: 18px; font-weight: 800; color: #2c3e50; margin-bottom: 10px; min-height: 50px; }
.fjc-gg-row { display: flex; justify-content: space-between; align-items: center; }
.fjc-gg { color: #145efc; font-weight: 700; }
.fjc-score { color: white; font-weight: 700; padding: 4px 10px; border-radius: 12px; font-size: 0.9rem; }
.meta-cell { border-top: 1px solid #eee; border-bottom: 1px solid #eee; font-size: 0.85rem; color: #555; min-height: 120px; }
.meta-row { margin-bottom: 5px; }
.section-cell { border-left-width: 5px; border-left-style: solid; border-top: none; background: #fdfdfd; }
.section-title { font-weight: 700; font-size: 0.95rem; margin-bottom: 8px; color: #333; display: flex; align-items: center; gap: 5px;}
.section-content { color: #444; font-size: 0.9rem; line-height: 1.5; white-space: pre-wrap; }
.footer-cell { height: 10px; border-top: none; border-radius: 0 0 12px 12px; background: #fff; }
.ai-insight-box { background-color: #eef6fc; border-left: 5px solid #145efc; padding: 15px 20px; border-radius: 8px; margin: 20px 0; color: #2c3e50; }
.ai-insight-title { font-weight: 800; color: #145efc; display: flex; align-items: center; gap: 8px; margin-bottom: 5px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
  <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/checkmark%20success.png" alt="icon">
  Job Match - Análise Semântica de Cargo
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 3. CARGA DE MODELO, DADOS E CONFIGS
# ===========================================================
MODEL_NAME = 'paraphrase-multilingual-MiniLM-L12-v2'  # mantém leve e rápido
ALPHA_SEMANTIC = 0.75  # peso da similaridade semântica no score final
GG_PENALTY_STEP = 0.05  # penalização por distância de GG

# pesos por seção para média ponderada de embeddings
W_SUBFAM = 1.0
W_JOBDESC = 1.0  # Job Profile Description
W_ROLE = 1.0
W_GRADE = 0.8
W_QUALIF = 0.8
W_BAND = 0.2

@st.cache_resource
def load_model():
    return SentenceTransformer(MODEL_NAME)

@st.cache_data(show_spinner=False)
def load_wtw_data():
    try:
        with open("data/wtw_job_match.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

@st.cache_data(show_spinner=False)
def prepare_data():
    data = load_excel_data()
    df_jobs = data.get("job_profile", pd.DataFrame()).fillna("")
    df_levels = data.get("level_structure", pd.DataFrame()).fillna("")

    if not df_jobs.empty:
        df_jobs.columns = df_jobs.columns.str.strip()
        needed = [
            "Job Family","Sub Job Family","Job Profile","Role Description","Grade Differentiator",
            "Qualifications","Global Grade","Career Path","Sub Job Family Description","Job Profile Description",
            "Career Band Description","Function","Discipline","Full Job Code","KPIs / Specific Parameters"
        ]
        for c in needed:
            if c not in df_jobs.columns:
                df_jobs[c] = "-"

    # normalização de GG
    df_jobs["Global Grade Num"] = pd.to_numeric(
        df_jobs["Global Grade"].astype(str).str.replace(r"\.0$","",regex=True),
        errors='coerce'
    ).fillna(0).astype(int)
    df_jobs["Global Grade"] = df_jobs["Global Grade Num"].astype(str)

    if "Global Grade" in df_levels.columns:
        df_levels["Global Grade"] = (
            df_levels["Global Grade"].astype(str).str.replace(r"\.0$","",regex=True).str.strip()
        )

    # textos por seção (usados na média ponderada)
    def nz(x):  # evita 'nan'
        s = str(x) if pd.notna(x) else ""
        return "-" if s.strip() == "" else s

    df_jobs["__sec_subdesc"] = df_jobs["Sub Job Family Description"].apply(nz)
    df_jobs["__sec_jobdesc"] = df_jobs["Job Profile Description"].apply(nz)
    df_jobs["__sec_role"] = df_jobs["Role Description"].apply(nz)
    df_jobs["__sec_grade"] = df_jobs["Grade Differentiator"].apply(nz)
    df_jobs["__sec_qualif"] = df_jobs["Qualifications"].apply(nz)
    df_jobs["__sec_band"] = df_jobs["Career Band Description"].apply(nz)

    # texto completo para TF-IDF
    df_jobs["Rich_Text"] = (
        "Sub Job Family Description: " + df_jobs["__sec_subdesc"] + ". " +
        "Job Profile: " + df_jobs["Job Profile"] + ". " +
        "Job Profile Description: " + df_jobs["__sec_jobdesc"] + ". " +
        "Role Description: " + df_jobs["__sec_role"] + ". " +
        "Grade Differentiator: " + df_jobs["__sec_grade"] + ". " +
        "Qualifications: " + df_jobs["__sec_qualif"] + ". " +
        "Career Band Description: " + df_jobs["__sec_band"] + ". " +
        "KPIs: " + df_jobs["KPIs / Specific Parameters"].apply(nz)
    )

    return df_jobs, df_levels

@st.cache_data(show_spinner=False)
def compute_weighted_embeddings(df_jobs):
    """
    Gera embeddings por seção e combina por média ponderada.
    Retorna matriz [n_jobs, dim].
    """
    model = load_model()
    # encode por seção com progress desativado p/ velocidade
    e_sub = model.encode(df_jobs["__sec_subdesc"].tolist(), show_progress_bar=False, batch_size=32)
    e_job = model.encode(df_jobs["__sec_jobdesc"].tolist(), show_progress_bar=False, batch_size=32)
    e_role = model.encode(df_jobs["__sec_role"].tolist(), show_progress_bar=False, batch_size=32)
    e_grade = model.encode(df_jobs["__sec_grade"].tolist(), show_progress_bar=False, batch_size=32)
    e_qual = model.encode(df_jobs["__sec_qualif"].tolist(), show_progress_bar=False, batch_size=32)
    e_band = model.encode(df_jobs["__sec_band"].tolist(), show_progress_bar=False, batch_size=32)

    weights = np.array([W_SUBFAM, W_JOBDESC, W_ROLE, W_GRADE, W_QUALIF, W_BAND], dtype=np.float32)
    weights = weights / (weights.sum() if weights.sum() > 0 else 1.0)

    # média ponderada dos vetores
    emb = (
        e_sub * weights[0] +
        e_job * weights[1] +
        e_role * weights[2] +
        e_grade * weights[3] +
        e_qual * weights[4] +
        e_band * weights[5]
    )
    return emb

@st.cache_resource
def build_tfidf(df_jobs):
    """
    Vetorizador TF-IDF treinado no Rich_Text para reforçar termos técnicos.
    """
    vect = TfidfVectorizer(
        max_features=30000,
        ngram_range=(1,2),
        strip_accents='unicode',
        lowercase=True
    )
    X = vect.fit_transform(df_jobs["Rich_Text"].tolist())
    return vect, X

try:
    df, df_levels = prepare_data()
    job_embeddings = compute_weighted_embeddings(df)
    wtw_data = load_wtw_data()
    model = load_model()
    tfidf_vect, tfidf_matrix = build_tfidf(df)
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

# ===========================================================
# 4. LÓGICA DE MATCHING (com heurísticas de mercado)
# ===========================================================
LEVEL_GG_MAPPING = {
    "W1":[1,2,3,4,5],"W2":[5,6,7,8],"W3":[7,8,9,10],
    "U1":[4,5,6,7],"U2":[6,7,8,9],"U3":[8,9,10,11],
    "P1":[8,9,10],"P2":[10,11,12],"P3":[12,13,14],"P4":[14,15,16,17],
    "M1":[11,12,13,14],"M2":[14,15,16],"M3":[16,17,18,19],
    "E1":[18,19,20,21],"E2":[21,22,23,24,25]
}

MGMT_PATTERNS = {
    "leadership": [
        r"\blidera\b", r"\bcoordena\b", r"\bgest[aã]o\b", r"\bmanage(s|r)?\b", r"\bsupervis(a|e)\b",
        r"\bteam lead\b", r"\bheading\b", r"\bdirige\b"
    ],
    "span_control": [
        r"\b(\d{1,3})\s*(report|diret[oa]s?|subordinad[oa]s?)\b", r"\bteam of\b", r"\bmanage(s)?\s+\d+"
    ],
    "budget": [
        r"\bor[cç]amento\b", r"\bbudget\b", r"\bP&L\b", r"\bcapex\b", r"\bOPEX\b"
    ],
    "strategy": [
        r"\bestr(at[eé]gia|ategic)\b", r"\bdefine\b\s+estrat[eé]gia", r"\broadmap\b", r"\bplanejamento\b"
    ],
    "ic_signals": [
        r"\bexecu[cç][aã]o\b", r"\bhands?-?on\b", r"\bopera[cç][aã]o\b", r"\ban[aá]lise\b", r"\bexecut(a|e)\b"
    ]
}

def market_level_heuristics(text: str) -> dict:
    """
    Heurísticas de mercado para diferenciar IC vs Gestão vs Executivo.
    Retorna contagem por eixo e um palpite de banda ('W/U/P' ~ IC; 'M' ~ gestão; 'E' ~ executivo).
    """
    t = text.lower()
    score_lead = sum(len(re.findall(p, t)) for p in MGMT_PATTERNS["leadership"])
    score_span = sum(len(re.findall(p, t)) for p in MGMT_PATTERNS["span_control"])
    score_budget = sum(len(re.findall(p, t)) for p in MGMT_PATTERNS["budget"])
    score_strategy = sum(len(re.findall(p, t)) for p in MGMT_PATTERNS["strategy"])
    score_ic = sum(len(re.findall(p, t)) for p in MGMT_PATTERNS["ic_signals"])

    mgmt_strength = score_lead + score_span + score_budget + score_strategy
    ic_strength = score_ic

    # palpite simples de banda
    if mgmt_strength >= 3 and score_budget >= 1:
        guess = "E"  # executivo se liderança + orçamento/estratégia fortes
    elif mgmt_strength >= 2:
        guess = "M"  # gestão
    else:
        guess = "P"  # individual contributor (profissional)

    return {
        "lead": score_lead, "span": score_span, "budget": score_budget, "strategy": score_strategy,
        "ic": score_ic, "mgmt_strength": mgmt_strength, "ic_strength": ic_strength, "guess_band": guess
    }

def detect_level_from_text(text, wtw_db):
    """
    WTW + heurísticas de mercado:
    - Usa o dicionário de career_bands/levels da WTW por keywords (core=+3, user=+1).
    - Aplica heurística para ajustar banda (P/M/E) quando evidente.
    """
    if not wtw_db or not text:
        return None, None, None, []

    text_lower = text.lower()
    best_score = 0
    best_band = None
    best_level = None
    best_key = None
    matched_keywords = []

    # 1) WTW scoring
    for _, band_info in wtw_db.get("career_bands", {}).items():
        for lvl_key, lvl_info in band_info.get("levels", {}).items():
            current_score = 0
            current_matches = []
            for kw in lvl_info.get("core_keywords", []):
                if re.search(r'\b' + re.escape(kw.lower()) + r'\b', text_lower):
                    current_score += 3
                    current_matches.append(kw)
            for ukw in lvl_info.get("user_keywords", []):
                if ukw.lower() in text_lower:
                    current_score += 1
                    current_matches.append(ukw)
            if current_score > best_score:
                best_score = current_score
                best_band = band_info
                best_level = lvl_info
                best_key = lvl_key
                matched_keywords = list(set(current_matches))

    # 2) heurística de mercado (ajuste de banda quando texto é muito claro)
    h = market_level_heuristics(text)
    if best_band and "label" in best_band:
        wtw_label = best_band["label"].upper()  # ex: "Professional", "Management", "Executive"
        # mapeia label -> inicial
        if "EXEC" in wtw_label:
            wtw_band_guess = "E"
        elif "MANAG" in wtw_label:
            wtw_band_guess = "M"
        else:
            wtw_band_guess = "P"
        # se heurística for muito forte, permite ajustar o nível-chave para um próximo mais coerente
        if h["guess_band"] == "E" and wtw_band_guess in ("M", "P"):
            # tenta promover para um nível executivo próximo (se existir no JSON)
            for key in ["E2","E1","M3","M2","M1","P4","P3","P2","P1","U3","U2","U1","W3","W2","W1"]:
                if key in LEVEL_GG_MAPPING:
                    best_key = best_key or key
        elif h["guess_band"] == "M" and wtw_band_guess == "P":
            for key in ["M2","M1","P4","P3","P2","P1"]:
                if key in LEVEL_GG_MAPPING:
                    best_key = best_key or key

    return best_band, best_level, best_key, matched_keywords

def gg_penalty_factor(gg_job: int, allowed_grades: list) -> float:
    """
    Penalização suave quando o GG do cargo se distancia do GG médio esperado para o nível.
    """
    if not allowed_grades:
        return 1.0
    target = int(np.median(allowed_grades))
    diff = abs(int(gg_job) - target)
    penalty = max(0.7, 1.0 - GG_PENALTY_STEP * diff)  # nunca cai abaixo de 0.7
    return penalty

# ===========================================================
# 5. INTERFACE DO USUÁRIO (inalterada)
# ===========================================================
st.markdown("Encontre o cargo ideal com base na descrição completa das responsabilidades.")

c1, c2 = st.columns(2)
with c1:
    families = sorted(df["Job Family"].unique())
    selected_family = st.selectbox("📂 Família (Obrigatório)", ["Selecione..."] + families)
with c2:
    subfamilies = sorted(df[df["Job Family"] == selected_family]["Sub Job Family"].unique()) if selected_family != "Selecione..." else []
    selected_subfamily = st.selectbox("📂 Subfamília (Obrigatório)", ["Selecione..."] + subfamilies)

desc_input = st.text_area(
    "📋 Cole aqui a descrição detalhada da posição (Mínimo 50 palavras):",
    height=200,
    placeholder="Descreva as principais responsabilidades, escopo de atuação, nível de autonomia..."
)
word_count = len(desc_input.strip().split())
st.caption(f"Contagem de palavras: {word_count} / 50")

# ===========================================================
# 6. EXECUÇÃO DO MATCH (mesmo botão / mesma UI)
# ===========================================================
if st.button("🔍 Analisar Aderência", type="primary", use_container_width=True):
    if selected_family == "Selecione..." or selected_subfamily == "Selecione..." or word_count < 50:
        st.warning("⚠️ Para uma análise precisa, selecione Família, Subfamília e insira uma descrição com pelo menos 50 palavras.")
        st.stop()

    # filtro por família/subfamília
    mask = (df["Job Family"] == selected_family) & (df["Sub Job Family"] == selected_subfamily)

    # nível detectado (WTW + heurística mercado)
    detected_band, detected_level, detected_key, keywords_found = detect_level_from_text(desc_input, wtw_data)
    allowed_grades = []
    if detected_key and detected_key in LEVEL_GG_MAPPING:
        allowed_grades = LEVEL_GG_MAPPING[detected_key]
        mask &= df["Global Grade Num"].isin(allowed_grades)
        kws_formatted = ", ".join([f"'{k}'" for k in keywords_found[:6]])
        st.markdown(f"""
        <div class="ai-insight-box">
            <div class="ai-insight-title">🤖 Análise Semântica de Nível</div>
            Com base na sua descrição, identificamos características de um nível
            <strong>{detected_level['label'] if detected_level and 'label' in detected_level else detected_key}</strong>
            (Carreira: {detected_band['label'] if detected_band and 'label' in detected_band else '—'}).<br>
            <small>Filtrando resultados para Grades coerentes: {min(allowed_grades) if allowed_grades else '-'} a {max(allowed_grades) if allowed_grades else '-'}.
            Termos detectados: {kws_formatted}.</small>
        </div>
        """, unsafe_allow_html=True)

    if not mask.any():
        st.error("Não foram encontrados cargos compatíveis com os filtros e o nível detectado.")
        st.stop()

    filtered_indices = df[mask].index
    filtered_embeddings = job_embeddings[filtered_indices]

    # embedding da consulta — média ponderada por seções
    def build_query_sections(text: str) -> dict:
        # para reforçar contexto técnico e senioridade, usamos o mesmo esquema de pesos
        return {
            "sub": text, "jobdesc": text, "role": text,
            "grade": text, "qual": text, "band": text
        }

    q_secs = build_query_sections(desc_input)
    q_embs = [
        load_model().encode([q_secs["sub"]], show_progress_bar=False),
        load_model().encode([q_secs["jobdesc"]], show_progress_bar=False),
        load_model().encode([q_secs["role"]], show_progress_bar=False),
        load_model().encode([q_secs["grade"]], show_progress_bar=False),
        load_model().encode([q_secs["qual"]], show_progress_bar=False),
        load_model().encode([q_secs["band"]], show_progress_bar=False),
    ]
    w = np.array([W_SUBFAM, W_JOBDESC, W_ROLE, W_GRADE, W_QUALIF, W_BAND], dtype=np.float32)
    w = w / (w.sum() if w.sum() > 0 else 1.0)
    query_emb = (q_embs[0]*w[0] + q_embs[1]*w[1] + q_embs[2]*w[2] + q_embs[3]*w[3] + q_embs[4]*w[4] + q_embs[5]*w[5])[0]

    # similaridade semântica
    sims_sem = cosine_similarity([query_emb], filtered_embeddings)[0]

    # similaridade TF-IDF (reforço de termos técnicos)
    q_tfidf = tfidf_vect.transform([desc_input])
    sims_kw = cosine_similarity(q_tfidf, tfidf_matrix[filtered_indices])[0]

    # score híbrido + penalização hierárquica
    scores = []
    for i, idx in enumerate(filtered_indices):
        gg_job = int(df.loc[idx, "Global Grade Num"])
        penalty = gg_penalty_factor(gg_job, allowed_grades)
        hybrid = (ALPHA_SEMANTIC * sims_sem[i] + (1 - ALPHA_SEMANTIC) * sims_kw[i]) * penalty
        scores.append(hybrid)

    results = df.loc[filtered_indices].copy()
    results["similarity"] = np.array(scores, dtype=float)
    top3 = results.sort_values("similarity", ascending=False).head(3)

    # ===========================================================
    # 7. RENDERIZAÇÃO (inalterada)
    # ===========================================================
    st.markdown("---")
    st.subheader("🏆 Cargos Mais Compatíveis")

    if len(top3) < 1:
        st.warning("Nenhum resultado encontrado.")
        st.stop()

    cards_data = []
    for _, row in top3.iterrows():
        score_val = float(row["similarity"]) * 100
        score_bg = "#28a745" if score_val > 85 else "#1E56E0" if score_val > 75 else "#fd7e14" if score_val > 60 else "#dc3545"
        lvl_name = ""
        gg_val = str(row["Global Grade"]).strip()
        if not df_levels.empty and "Global Grade" in df_levels.columns and "Level Name" in df_levels.columns:
            match = df_levels[df_levels["Global Grade"].astype(str).str.strip() == gg_val]
            if not match.empty:
                lvl_name = f"• {match['Level Name'].iloc[0]}"
        cards_data.append({"row": row, "score_fmt": f"{score_val:.1f}%", "score_bg": score_bg, "lvl": lvl_name})

    num_results = len(cards_data)
    grid_style = f"grid-template-columns: repeat({num_results}, 1fr);"
    grid_html = f'<div class="comparison-grid" style="{grid_style}">'

    # 1. Cabeçalho
    for card in cards_data:
        grid_html += f"""
        <div class="grid-cell header-cell">
            <div class="fjc-title">{html.escape(card['row']['Job Profile'])}</div>
            <div class="fjc-gg-row">
                <div class="fjc-gg">GG {card['row']['Global Grade']} {card['lvl']}</div>
                <div class="fjc-score" style="background-color: {card['score_bg']};">{card['score_fmt']} Match</div>
            </div>
        </div>"""

    # 2. Metadados
    for card in cards_data:
        d = card['row']
        grid_html += f"""
        <div class="grid-cell meta-cell">
            <div class="meta-row"><strong>Família:</strong> {html.escape(str(d.get('Job Family','-')))}</div>
            <div class="meta-row"><strong>Subfamília:</strong> {html.escape(str(d.get('Sub Job Family','-')))}</div>
            <div class="meta-row"><strong>Carreira:</strong> {html.escape(str(d.get('Career Path','-')))}</div>
            <div class="meta-row"><strong>Cód:</strong> {html.escape(str(d.get('Full Job Code','-')))}</div>
        </div>"""

    # 3. Seções (inalteradas)
    sections_config = [
        ("🧭 Sub Job Family Description", "Sub Job Family Description", "#95a5a6"),
        ("🧠 Job Profile Description", "Job Profile Description", "#e91e63"),
        ("🏛️ Career Band Description", "Career Band Description", "#673ab7"),
        ("🎯 Role Description", "Role Description", "#145efc"),
        ("🏅 Grade Differentiator", "Grade Differentiator", "#ff9800"),
        ("🎓 Qualifications", "Qualifications", "#009688")
    ]

    for title, field, color in sections_config:
        for card in cards_data:
            content = str(card['row'].get(field, '-'))
            if field == "Qualifications" and (len(content) < 2 or content.lower() == 'nan'):
                grid_html += '<div class="grid-cell section-cell" style="border-left-color: transparent; background: transparent; border: none;"></div>'
            else:
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

    # feedback sobre aderência (baseado no híbrido)
    if float(top3.iloc[0]["similarity"]) < 0.6:
        st.info("💡 Aderência moderada. Tente refinar sua descrição.")
