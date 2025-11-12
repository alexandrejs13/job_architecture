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
# 🔹 Carregamento das regras de negócio da arquitetura de cargos
# ===========================================================
try:
    with open("data/job_rules.json", "r", encoding="utf-8") as f:
        job_rules = json.load(f)
except FileNotFoundError:
    st.warning("⚠️ Arquivo de regras `data/job_rules.json` não encontrado. As regras personalizadas não serão aplicadas.")
    job_rules = {}
except Exception as e:
    st.error(f"Erro ao carregar `job_rules.json`: {e}")
    job_rules = {}

# ===========================================================
# 🔹 Função de aplicação de regras de negócio
# ===========================================================
def apply_business_rules(input_text, candidate, metadata, job_rules):
    """Aplica regras de negócio ao cálculo de similaridade entre o texto e o perfil de cargo."""
    weight = 1.0
    text = str(input_text).lower()
    cand = str(candidate).lower()

    # Hierarquia
    hierarchy = {
        "auxiliar": 1, "assistente": 2, "analista": 3, "especialista": 4,
        "coordenador": 5, "supervisor": 5, "gerente": 6,
        "gerente senior": 7, "diretor": 8, "head": 8
    }

    def detect_level(txt):
        for k, v in hierarchy.items():
            if k in txt:
                return v
        return 0

    user_level = detect_level(text)
    cand_level = detect_level(cand)

    if user_level and cand_level:
        if cand_level > user_level + 1:
            weight *= 0.4
        elif cand_level < user_level - 2:
            weight *= 0.6
        elif cand_level == user_level:
            weight *= 1.1

    # Gestão de equipe
    if "sem equipe" in text or "individual" in text or "profissional" in text:
        if any(k in cand for k in ["manager", "gerente", "coordenador"]):
            weight *= 0.5
    else:
        if any(k in cand for k in ["manager", "gerente", "coordenador"]):
            weight *= 1.1

    # Abrangência
    if "regional" in text:
        weight *= 1.1
    elif "global" in text:
        weight *= 1.2
    elif "local" in text:
        weight *= 0.9

    # Múltiplas áreas
    if any(x in text for x in ["diversas áreas", "multiplas funções", "abrangência ampla"]):
        weight *= 1.15

    # Regras adicionais do JSON
    for rule in job_rules.get("rules", []):
        keywords = [k.lower() for k in rule.get("keywords", [])]
        multiplier = rule.get("multiplier", 1.0)
        if any(k in text for k in keywords):
            weight *= multiplier

    return weight

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
# 2. CSS GLOBAL
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
.comparison-grid { display: grid; gap: 20px; margin-top: 20px; }
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
.fjc-title { font-size: 18px; font-weight: 800; color: #2c3e50; margin-bottom: 2px; min-height: 50px; }
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
# 3. CARREGAMENTO DE DADOS E MODELO
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

df, df_levels = load_data()
model = load_model()

# ===========================================================
# 4. INTERFACE E ANÁLISE
# ===========================================================
st.markdown("### 🧠 Descrição do Cargo para Análise")
desc_input = st.text_area("📝 Digite ou cole a descrição do cargo:", height=180)

if st.button("🔍 Analisar Aderência", type="primary", use_container_width=True):
    if len(desc_input.split()) < 50:
        st.warning("Por favor, insira ao menos 50 palavras.")
        st.stop()

    job_texts = (df["Job Profile"].fillna("") + ". " + df["Role Description"].fillna("") + ". " + df["Qualifications"].fillna("")).tolist()
    job_emb = model.encode(job_texts, show_progress_bar=False)
    query_emb = model.encode([desc_input], show_progress_bar=False)[0]
    sims_sem = cosine_similarity([query_emb], job_emb)[0]

    tfidf = TfidfVectorizer(max_features=10000, ngram_range=(1, 2)).fit(job_texts)
    job_tfidf = tfidf.transform(job_texts)
    query_tfidf = tfidf.transform([desc_input])
    sims_kw = cosine_similarity(query_tfidf, job_tfidf)[0]

    sims = 0.75 * sims_sem + 0.25 * sims_kw

    # ➕ Aplica regras de negócio no peso de similaridade
    for i, row in df.iterrows():
        sims[i] *= apply_business_rules(desc_input, row["Job Profile"], row.to_dict(), job_rules)

    df["similarity"] = sims
    top3 = df.sort_values("similarity", ascending=False).head(3)

    st.markdown("---")
    st.header("🏆 Cargos Mais Compatíveis")

    if top3.empty:
        st.warning("Nenhum resultado encontrado.")
        st.stop()

    for _, row in top3.iterrows():
        st.markdown(f"""
        <div class="ai-insight-box">
            <div class="ai-insight-title">🎯 {html.escape(row['Job Profile'])}</div>
            <b>Similaridade:</b> {row['similarity']*100:.1f}%<br>
            <b>Global Grade:</b> {row['Global Grade']}<br>
            <b>Família:</b> {row['Job Family']} | <b>Sub-Família:</b> {row['Sub Job Family']}
        </div>
        """, unsafe_allow_html=True)
