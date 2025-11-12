# -*- coding: utf-8 -*-
# pages/5_🧩_Job_Match.py

import streamlit as st
import pandas as pd
import html
import json
import re
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from utils.ui import sidebar_logo_and_title

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
# 2. CSS GLOBAL E HEADER
# ===========================================================
css_path = Path(__file__).parents[1] / "assets" / "header.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

sidebar_logo_and_title()

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
    max-width: 1200px !important;
    padding-left: 40px !important;
    padding-right: 40px !important;
}

.match-card {
    background: #fff;
    border-left: 5px solid #145efc;
    border-radius: 12px;
    padding: 24px 28px;
    margin-top: 25px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.08);
}
.match-score {
    font-weight: 800;
    font-size: 1.25rem;
    color: #145efc;
}
</style>

<div class="page-header">
  <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/process.png" alt="icon">
  Job Match — Similaridade de Perfis
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 3. FUNÇÕES AUXILIARES
# ===========================================================

@st.cache_resource
def load_model():
    return SentenceTransformer("paraphrase-MiniLM-L6-v2")

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

@st.cache_data
def load_excel(path):
    try:
        df = pd.read_excel(path)
        for c in df.select_dtypes(include="object"):
            df[c] = df[c].astype(str).str.strip()
        return df
    except Exception as e:
        st.error(f"Erro ao carregar {path}: {e}")
        return pd.DataFrame()

def calculate_similarity(text1, text2, model):
    if not text1 or not text2:
        return 0.0
    embeddings = model.encode([text1, text2])
    return float(cosine_similarity([embeddings[0]], [embeddings[1]])[0][0])

# Ajusta a similaridade com base nas regras de coerência
def adjust_similarity(base_score, job_a, job_b, rules):
    adjusted = base_score
    try:
        # Normaliza
        ja, jb = job_a.lower(), job_b.lower()

        # Checa tipo de liderança
        for leadership_type, positions in rules.get("leadership_type", {}).items():
            if any(p.lower() in ja for p in positions) and any(p.lower() in jb for p in positions):
                adjusted += 0.05

        # Checa hierarquia coerente
        hierarchy = rules.get("hierarchy", {})
        if hierarchy:
            a_val = next((v for k, v in hierarchy.items() if k.lower() in ja), None)
            b_val = next((v for k, v in hierarchy.items() if k.lower() in jb), None)
            if a_val and b_val:
                diff = abs(a_val - b_val)
                if diff == 0:
                    adjusted += 0.05
                elif diff == 1:
                    adjusted += 0.02
                elif diff > 2:
                    adjusted -= 0.05

        # Checa escopo
        for scope, positions in rules.get("scope", {}).items():
            if any(p.lower() in ja for p in positions) and any(p.lower() in jb for p in positions):
                adjusted += 0.03

    except Exception:
        pass

    return max(0, min(adjusted, 1.0))

# ===========================================================
# 4. DADOS E REGRAS
# ===========================================================
df_profiles = load_excel("data/Job Profile.xlsx")
model = load_model()

rules_path = Path("data/job_rules.json")
if rules_path.exists():
    with open(rules_path, "r", encoding="utf-8") as f:
        job_rules = json.load(f)
else:
    job_rules = {}

if df_profiles.empty:
    st.error("❌ Arquivo 'Job Profile.xlsx' não encontrado ou inválido.")
    st.stop()

# ===========================================================
# 5. INTERFACE — INPUT DO USUÁRIO
# ===========================================================
st.markdown("### Descreva o perfil que deseja comparar:")

col1, col2 = st.columns(2)
with col1:
    job_title = st.text_input("Título do cargo:", placeholder="Ex: HR Business Partner Senior")
with col2:
    job_scope = st.selectbox("Escopo:", ["Global", "Regional", "Local", "Não se aplica"], index=3)

job_desc = st.text_area("Descrição do cargo:", height=180, placeholder="Cole aqui a descrição completa do cargo...")

if not job_desc.strip():
    st.info("✏️ Insira a descrição para realizar o Job Match.")
    st.stop()

# ===========================================================
# 6. PROCESSAMENTO — SIMILARIDADE
# ===========================================================
model = load_model()

df_profiles["text_concat"] = df_profiles[
    ["Job Profile Description", "Role Description", "Sub Job Family Description"]
].astype(str).agg(" ".join, axis=1)

# Calcula similaridade base e ajusta com as regras
results = []
for _, row in df_profiles.iterrows():
    ref_text = clean_text(row["text_concat"])
    base_sim = calculate_similarity(clean_text(job_desc), ref_text, model)
    adjusted_sim = adjust_similarity(base_sim, job_title, row.get("Job Profile", ""), job_rules)

    results.append({
        "Job Profile": row.get("Job Profile", ""),
        "Job Family": row.get("Job Family", ""),
        "Sub Job Family": row.get("Sub Job Family", ""),
        "Career Path": row.get("Career Path", ""),
        "Global Grade": row.get("Global Grade", ""),
        "Similarity": adjusted_sim
    })

df_results = pd.DataFrame(results).sort_values(by="Similarity", ascending=False).head(5)

# ===========================================================
# 7. EXIBIÇÃO DE RESULTADOS
# ===========================================================
st.markdown("## 🔍 Resultados do Job Match")

for _, r in df_results.iterrows():
    st.markdown(f"""
    <div class="match-card">
        <div class="match-score">🎯 Similaridade: {r['Similarity']*100:.1f}%</div>
        <b>{r['Job Profile']}</b><br>
        <small>
        Família: {r['Job Family']}<br>
        Sub-Família: {r['Sub Job Family']}<br>
        Trilha: {r['Career Path']}<br>
        Global Grade: {r['Global Grade']}
        </small>
    </div>
    """, unsafe_allow_html=True)
