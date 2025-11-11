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
# 1. CONFIGURAÇÃO DE PÁGINA
# ===========================================================
st.set_page_config(layout="wide", page_title="🧩 Job Match", page_icon="✅")

# ===========================================================
# 2. CSS E SIDEBAR
# ===========================================================
css_path = Path(__file__).parents[1] / "assets" / "header.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

setup_sidebar()
lock_sidebar()

st.markdown("""
<div class="page-header" style="background-color:#145efc;color:white;font-weight:750;font-size:1.35rem;border-radius:12px;padding:22px 36px;display:flex;align-items:center;gap:18px;width:100%;margin-bottom:40px;box-shadow:0 4px 12px rgba(0,0,0,0.15);">
  <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/checkmark%20success.png" style="width:48px;height:48px;" alt="icon">
  Job Match - Análise Semântica de Cargo
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 3. CARREGAMENTO DE DADOS E MODELO
# ===========================================================
@st.cache_resource
def load_model():
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

@st.cache_data(show_spinner=False)
def load_wtw_data():
    try:
        with open("data/wtw_job_match.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

@st.cache_data(show_spinner=False)
def prepare_data():
    data = load_excel_data()
    df_jobs = data.get("job_profile", pd.DataFrame()).fillna("")
    df_levels = data.get("level_structure", pd.DataFrame()).fillna("")
    df_jobs.columns = df_jobs.columns.str.strip()
    if "Global Grade" in df_jobs.columns:
        df_jobs["Global Grade Num"] = pd.to_numeric(df_jobs["Global Grade"], errors='coerce').fillna(0).astype(int)
    else:
        df_jobs["Global Grade Num"] = 0
    return df_jobs, df_levels

df, df_levels = prepare_data()
model = load_model()
wtw_data = load_wtw_data()

# ===========================================================
# 4. CAMPOS DE ENTRADA HIERÁRQUICOS (WTW)
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
# 5. CAMPOS DE FAMÍLIA E DESCRIÇÃO
# ===========================================================
st.markdown("### 🧠 Contexto Funcional e Descrição do Cargo")

c1, c2 = st.columns(2)
with c1:
    families = sorted(df["Job Family"].unique())
    selected_family = st.selectbox("📂 Família (Obrigatório)", ["Selecione..."] + families)
with c2:
    subfamilies = sorted(df[df["Job Family"] == selected_family]["Sub Job Family"].unique()) if selected_family != "Selecione..." else []
    selected_subfamily = st.selectbox("📂 Subfamília (Obrigatório)", ["Selecione..."] + subfamilies)

desc_input = st.text_area("📝 Descrição detalhada do cargo (mínimo 50 palavras):", height=200)
word_count = len(desc_input.strip().split())
st.caption(f"Contagem de palavras: {word_count} / 50")

# ===========================================================
# 6. MAPEAMENTO DE NÍVEIS E FUNÇÃO DE INFERÊNCIA
# ===========================================================
LEVEL_GG_MAPPING = {
    "W1": [1,2,3,4,5],"W2":[5,6,7,8],"W3":[7,8,9,10],
    "P1":[8,9,10],"P2":[10,11,12],"P3":[12,13,14],"P4":[14,15,16,17],
    "M1":[11,12,13,14],"M2":[14,15,16],"M3":[16,17,18,19],
    "E1":[18,19,20,21],"E2":[21,22,23,24,25]
}

def infer_market_level(superior, lidera, subordinados, abrangencia, multiplas_areas):
    if superior in ["Presidente / CEO", "Vice-presidente"]:
        return "E2"
    if superior == "Diretor" or abrangencia in ["Multipaís", "Global"]:
        return "E1"
    if superior == "Gerente":
        if lidera == "Sim" and subordinados in ["6-10","11-20","21-50","51-100","100+"]:
            return "M2"
        else:
            return "M1"
    if superior in ["Coordenador","Supervisor"]:
        return "P4"
    return "P2"

# ===========================================================
# 7. BOTÃO DE ANÁLISE (RESTABELECIDO)
# ===========================================================
st.divider()
st.markdown("### 🔎 Executar análise")

if st.button("🔍 Analisar Aderência", type="primary", use_container_width=True):

    if "Selecione..." in [superior,lidera,abrangencia,selected_family,selected_subfamily] or word_count < 50:
        st.warning("⚠️ Todos os campos obrigatórios devem ser preenchidos corretamente.")
        st.stop()

    detected_key = infer_market_level(superior,lidera,subordinados,abrangencia,multiplas_areas)
    allowed_grades = LEVEL_GG_MAPPING.get(detected_key, [])

    st.markdown(f"""
    <div class="ai-insight-box">
        <div class="ai-insight-title">🤖 Contexto Hierárquico Detectado</div>
        <strong>Banda sugerida:</strong> {detected_key} — conforme práticas WTW e parâmetros informados.<br>
        <small>Baseado em: reporte a {superior.lower()}, liderança = {lidera.lower()}, abrangência = {abrangencia.lower()}.</small>
    </div>
    """, unsafe_allow_html=True)

    mask = (df["Job Family"] == selected_family) & (df["Sub Job Family"] == selected_subfamily)
    if allowed_grades:
        mask &= df["Global Grade Num"].isin(allowed_grades)
    if not mask.any():
        st.error("Nenhum cargo encontrado dentro da família e subfamília informadas.")
        st.stop()

    filtered = df[mask].copy()
    job_texts = (filtered["Job Profile"].fillna("") + ". " +
                 filtered["Role Description"].fillna("") + ". " +
                 filtered["Qualifications"].fillna("")).tolist()

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
    # 8. RENDERIZAÇÃO VISUAL EM 3 COLUNAS
    # ===========================================================
    st.markdown("---")
    st.subheader("🏆 Cargos Mais Compatíveis")

    if len(top3) < 1:
        st.warning("Nenhum resultado encontrado.")
        st.stop()

    cards_data = []
    for _, row in top3.iterrows():
        score_val = float(row["similarity"]) * 100
        score_bg = (
            "#28a745" if score_val > 85
            else "#1E56E0" if score_val > 75
            else "#fd7e14" if score_val > 60
            else "#dc3545"
        )
        lvl_name = ""
        gg_val = str(row["Global Grade"]).strip()
        if not df_levels.empty and "Global Grade" in df_levels.columns and "Level Name" in df_levels.columns:
            match = df_levels[df_levels["Global Grade"].astype(str).str.strip() == gg_val]
            if not match.empty:
                lvl_name = f"• {match['Level Name'].iloc[0]}"
        cards_data.append({
            "row": row,
            "score_fmt": f"{score_val:.1f}%",
            "score_bg": score_bg,
            "lvl": lvl_name
        })

    grid_style = "grid-template-columns: repeat(3, 1fr);"
    grid_html = f'<div class="comparison-grid" style="{grid_style}">'

    # Cabeçalho
    for card in cards_data:
        grid_html += f"""
        <div class="grid-cell header-cell">
            <div class="fjc-title">{html.escape(card['row']['Job Profile'])}</div>
            <div class="fjc-gg-row">
                <div class="fjc-gg">GG {card['row']['Global Grade']} {card['lvl']}</div>
                <div class="fjc-score" style="background-color:{card['score_bg']};">{card['score_fmt']} Match</div>
            </div>
        </div>"""

    # Metadados
    for card in cards_data:
        d = card["row"]
        grid_html += f"""
        <div class="grid-cell meta-cell">
            <div class="meta-row"><strong>Família:</strong> {html.escape(str(d.get('Job Family','-')))}</div>
            <div class="meta-row"><strong>Subfamília:</strong> {html.escape(str(d.get('Sub Job Family','-')))}</div>
            <div class="meta-row"><strong>Carreira:</strong> {html.escape(str(d.get('Career Path','-')))}</div>
            <div class="meta-row"><strong>Cód:</strong> {html.escape(str(d.get('Full Job Code','-')))}</div>
        </div>"""

    # Seções coloridas
    sections = [
        ("🧭 Sub Job Family Description", "Sub Job Family Description", "#95a5a6"),
        ("🧠 Job Profile Description", "Job Profile Description", "#e91e63"),
        ("🏛️ Career Band Description", "Career Band Description", "#673ab7"),
        ("🎯 Role Description", "Role Description", "#145efc"),
        ("🏅 Grade Differentiator", "Grade Differentiator", "#ff9800"),
        ("🎓 Qualifications", "Qualifications", "#009688")
    ]
    for title, field, color in sections:
        for card in cards_data:
            content = str(card["row"].get(field, "-"))
            if field == "Qualifications" and (len(content) < 2 or content.lower() == "nan"):
                grid_html += '<div class="grid-cell section-cell" style="border-left-color: transparent; background: transparent; border: none;"></div>'
            else:
                grid_html += f"""
                <div class="grid-cell section-cell" style="border-left-color:{color};">
                    <div class="section-title" style="color:{color};">{title}</div>
                    <div class="section-content">{html.escape(content)}</div>
                </div>"""

    for _ in cards_data:
        grid_html += '<div class="grid-cell footer-cell"></div>'

    grid_html += "</div>"
    st.markdown(grid_html, unsafe_allow_html=True)

    if float(top3.iloc[0]["similarity"]) < 0.6:
        st.info("💡 Aderência moderada. Tente refinar sua descrição.")
