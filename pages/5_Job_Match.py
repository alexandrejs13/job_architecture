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

/* GRID ESTILO JOB PROFILE */
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
.fjc-score {
    color: #145efc;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 0.9rem;
}
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
.section-title {
    font-weight: 700;
    font-size: 0.95rem;
    margin-bottom: 8px;
    color: #333;
    display: flex;
    align-items: center;
    gap: 5px;
}
.section-content {
    color: #444;
    font-size: 0.9rem;
    line-height: 1.5;
    white-space: pre-wrap;
}
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
# 3. FUNÇÕES E MODELOS
# ===========================================================
@st.cache_resource
def load_model():
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

@st.cache_data
def load_data():
    data = load_excel_data()
    df_jobs = data.get("job_profile", pd.DataFrame()).fillna("")
    df_levels = data.get("level_structure", pd.DataFrame()).fillna("")
    if "Global Grade" in df_jobs.columns:
        df_jobs["Global Grade Num"] = pd.to_numeric(df_jobs["Global Grade"], errors="coerce").fillna(0).astype(int)
    return df_jobs, df_levels

# ===========================================================
# 4. AJUSTE DE SIMILARIDADE HIERÁRQUICA
# ===========================================================
def adjust_similarity(base_score, job_a, job_b, rules, context=None):
    adjusted = base_score
    try:
        ja, jb = job_a.lower(), job_b.lower()
        ctx = context or {}

        if ctx.get("has_team") == "Não":
            if any(x in jb for x in ["manager","supervisor","leader","head","gerente","líder","supervisor"]):
                adjusted -= 0.25
        elif ctx.get("has_team") == "Sim":
            if any(x in jb for x in ["manager","supervisor","leader","head","gerente","líder"]):
                adjusted += 0.05

        reports_to = str(ctx.get("reports_to","")).lower()
        hierarchy_map = rules.get("hierarchy", {})

        def level(label):
            for k,v in hierarchy_map.items():
                if k.lower() in label:
                    return v
            return None

        if reports_to:
            report_lvl = level(reports_to)
            job_lvl = level(jb)
            if report_lvl is not None and job_lvl is not None:
                if job_lvl >= report_lvl:
                    adjusted -= 0.3
                elif abs(job_lvl - report_lvl) == 1:
                    adjusted += 0.05

        scope_rules = rules.get("scope", {})
        scope_ctx = str(ctx.get("scope", "")).lower()
        for scope, titles in scope_rules.items():
            if scope.lower() == scope_ctx and any(t.lower() in jb for t in titles):
                adjusted += 0.03

        adjusted = max(0, min(adjusted, 1.0))
        if adjusted < 0.2: adjusted = 0.0
    except Exception:
        pass
    return adjusted

# ===========================================================
# 5. INTERFACE DE ENTRADA
# ===========================================================
df, df_levels = load_data()
model = load_model()

st.markdown("### 🔧 Parâmetros Hierárquicos e Organizacionais")
c1,c2,c3 = st.columns(3)
with c1:
    superior = st.selectbox("📋 Cargo ao qual reporta *", ["Selecione...","Supervisor","Coordenador","Gerente","Diretor","Vice-presidente","Presidente / CEO"])
with c2:
    lidera = st.selectbox("👥 Possui equipe? *", ["Selecione...","Sim","Não"])
with c3:
    abrangencia = st.selectbox("🌍 Abrangência da função *", ["Selecione...","Local","Regional","Nacional","Multipaís","Global"])

if lidera=="Sim":
    c4,c5 = st.columns(2)
    with c4: subordinados = st.selectbox("📈 Nº de subordinados diretos *",["0-5","6-10","11-20","21-50","51-100","100+"])
    with c5: multiplas_areas = st.selectbox("🏢 Responsável por múltiplas áreas / funções? *",["Não","Sim"])
else:
    subordinados="0"; multiplas_areas="Não"

st.divider()
st.markdown("### 🧠 Contexto Funcional e Descrição do Cargo")
c1,c2 = st.columns(2)
with c1:
    families = sorted(df["Job Family"].unique())
    selected_family = st.selectbox("📂 Família (Obrigatório)",["Selecione..."]+families)
with c2:
    subfamilies = sorted(df[df["Job Family"]==selected_family]["Sub Job Family"].unique()) if selected_family!="Selecione..." else []
    selected_subfamily = st.selectbox("📂 Subfamília (Obrigatório)",["Selecione..."]+subfamilies)

desc_input = st.text_area("📝 Descrição detalhada do cargo (mínimo 50 palavras):", height=200)
word_count = len(desc_input.strip().split())
st.caption(f"Contagem de palavras: {word_count} / 50")

# ===========================================================
# 6. REGRAS HIERÁRQUICAS E ANÁLISE
# ===========================================================
rules_path = Path("data/job_rules.json")
job_rules = json.load(open(rules_path, encoding="utf-8")) if rules_path.exists() else {}

context = {
    "reports_to": superior,
    "has_team": lidera,
    "scope": abrangencia
}

LEVEL_GG_MAPPING = {
    "W1":[1,2,3,4,5],"W2":[5,6,7,8],"W3":[7,8,9,10],
    "P1":[8,9,10],"P2":[10,11,12],"P3":[12,13,14],"P4":[14,15,16,17],
    "M1":[11,12,13,14],"M2":[14,15,16],"M3":[16,17,18,19],
    "E1":[18,19,20,21],"E2":[21,22,23,24,25]
}

def infer_market_level(superior,lidera,subordinados,abrangencia):
    if superior in ["Presidente / CEO","Vice-presidente"]: return "E2"
    if superior=="Diretor" or abrangencia in ["Multipaís","Global"]: return "E1"
    if superior=="Gerente":
        if lidera=="Sim" and subordinados not in ["0-5"]: return "M2"
        else: return "M1"
    if superior in ["Coordenador","Supervisor"]: return "P4"
    return "P2"

# ===========================================================
# 7. EXECUÇÃO
# ===========================================================
if st.button("🔍 Analisar Aderência", type="primary", use_container_width=True):
    if "Selecione..." in [superior,lidera,abrangencia,selected_family,selected_subfamily] or word_count<50:
        st.warning("⚠️ Todos os campos obrigatórios devem ser preenchidos corretamente.")
        st.stop()

    detected_key = infer_market_level(superior,lidera,subordinados,abrangencia)
    allowed_grades = LEVEL_GG_MAPPING.get(detected_key, [])

    st.markdown(f"""
    <div class="ai-insight-box">
    <div class="ai-insight-title">🤖 Contexto Hierárquico Detectado</div>
    <strong>Banda sugerida:</strong> {detected_key}<br>
    <small>Baseado em: reporte a {superior.lower()}, liderança = {lidera.lower()}, abrangência = {abrangencia.lower()}.</small>
    </div>
    """, unsafe_allow_html=True)

    mask = (df["Job Family"]==selected_family) & (df["Sub Job Family"]==selected_subfamily)
    if allowed_grades: mask &= df["Global Grade Num"].isin(allowed_grades)
    filtered = df[mask].copy()
    if filtered.empty:
        st.error("Nenhum cargo encontrado.")
        st.stop()

    job_texts = (filtered["Job Profile"].fillna("")+". "+filtered["Role Description"].fillna("")+". "+filtered["Qualifications"].fillna("")).tolist()
    job_emb = model.encode(job_texts, show_progress_bar=False)
    query_emb = model.encode([desc_input], show_progress_bar=False)[0]

    sims_sem = cosine_similarity([query_emb], job_emb)[0]
    tfidf = TfidfVectorizer(max_features=10000, ngram_range=(1,2)).fit(job_texts)
    sims_kw = cosine_similarity(tfidf.transform([desc_input]), tfidf.transform(job_texts))[0]
    sims = 0.75*sims_sem + 0.25*sims_kw

    filtered["similarity"] = [
        adjust_similarity(s, desc_input, j, job_rules, context)
        for s,j in zip(sims, filtered["Job Profile"])
    ]

    top3 = filtered.sort_values("similarity", ascending=False).head(3)
    if len(top3)<1:
        st.warning("Nenhum resultado coerente encontrado.")
        st.stop()

    # =======================================================
    # 8. GRID FINAL
    # =======================================================
    st.markdown("---")
    st.header("🏆 Cargos Mais Compatíveis")
    cards_data=[]
    for _,row in top3.iterrows():
        score_val=float(row["similarity"])*100
        lvl_name=""
        gg_val=str(row["Global Grade"]).strip()
        if not df_levels.empty:
            match=df_levels[df_levels["Global Grade"].astype(str).str.strip()==gg_val]
            if not match.empty: lvl_name=f"• {match['Level Name'].iloc[0]}"
        cards_data.append({
            "row":row,"score_fmt":f"{score_val:.1f}%","lvl":lvl_name
        })
    num_results=len(cards_data)
    grid_html=f'<div class="comparison-grid" style="grid-template-columns: repeat({num_results},1fr);">'
    sections_config=[
        ("🧭 Sub Job Family Description","Sub Job Family Description","#95a5a6"),
        ("🧠 Job Profile Description","Job Profile Description","#e91e63"),
        ("🏛️ Career Band Description","Career Band Description","#673ab7"),
        ("🎯 Role Description","Role Description","#145efc"),
        ("🏅 Grade Differentiator","Grade Differentiator","#ff9800"),
        ("🎓 Qualifications","Qualifications","#009688")
    ]
    for card in cards_data:
        grid_html += f"""
        <div class="grid-cell header-cell">
        <div class="fjc-title">{html.escape(card['row'].get('Job Profile','-'))}</div>
        <div class="fjc-gg-row"><div class="fjc-gg">GG {card['row'].get('Global Grade','-')} {card['lvl']}</div>
        <div class="fjc-score">{card['score_fmt']} Match</div></div></div>"""
    for card in cards_data:
        d=card['row']; meta=[]
        for lbl,col in [("Família","Job Family"),("Subfamília","Sub Job Family"),("Carreira","Career Path"),("Cód","Full Job Code")]:
            val=str(d.get(col,"") or "-").strip()
            meta.append(f'<div class="meta-row"><strong>{lbl}:</strong> {html.escape(val)}</div>')
        grid_html += f'<div class="grid-cell meta-cell">{"".join(meta)}</div>'
    for title,field,color in sections_config:
        for card in cards_data:
            content=str(card['row'].get(field,'-'))
            if len(content.strip())<2:
                grid_html+='<div class="grid-cell section-cell" style="border:none;background:transparent;"></div>'
            else:
                grid_html+=f"""
                <div class="grid-cell section-cell" style="border-left-color:{color};">
                <div class="section-title" style="color:{color};">{title}</div>
                <div class="section-content">{html.escape(content)}</div></div>"""
    for _ in cards_data: grid_html+='<div class="grid-cell footer-cell"></div>'
    grid_html+='</div>'
    st.markdown(grid_html, unsafe_allow_html=True)
