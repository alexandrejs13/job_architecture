# ===========================================================
# 5_JOB_MATCH.PY — COM REGRAS HIERÁRQUICAS, LIDERANÇA E ESCOPO
# ===========================================================

import streamlit as st
import pandas as pd
import json
import re
from sentence_transformers import SentenceTransformer, util
from pathlib import Path
from utils.ui import sidebar_logo_and_title

# ===========================================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ===========================================================
st.set_page_config(
    page_title="Job Match",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================================================
# 2. CARREGAR CSS GLOBAL E SIDEBAR
# ===========================================================
css_path = Path(__file__).parents[1] / "assets" / "header.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

sidebar_logo_and_title()

st.markdown("""
<div class="page-header">
  <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/checkmark%20success.png" width="48">
  Job Match — Sugestão de Cargos Compatíveis
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 3. CARREGAR DADOS E MODELO
# ===========================================================
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

@st.cache_data
def load_data():
    try:
        df = pd.read_excel("data/Job Profile.xlsx")
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Erro ao carregar Job Profile.xlsx: {e}")
        return pd.DataFrame()

@st.cache_data
def load_rules():
    try:
        with open("data/job_rules.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.warning(f"Regras não encontradas ({e})")
        return {}

model = load_model()
df = load_data()
rules = load_rules()

if df.empty:
    st.stop()

# ===========================================================
# 4. AJUSTE DE SIMILARIDADE
# ===========================================================
def normalize_text(t):
    return re.sub(r"[^a-z0-9 ]", "", str(t).lower())

def adjust_similarity(base_score, job_a, job_b, rules, context=None):
    adjusted = base_score
    try:
        ja, jb = job_a.lower(), job_b.lower()
        ctx = context or {}

        # === 1. Liderança ===
        if ctx.get("has_team") == "Não":
            if any(x in jb for x in ["manager", "supervisor", "leader", "head", "coordinator", "gerente", "líder"]):
                adjusted -= 0.25
        elif ctx.get("has_team") == "Sim":
            if any(x in jb for x in ["manager", "supervisor", "leader", "head", "gerente", "líder"]):
                adjusted += 0.05

        # === 2. Hierarquia ===
        reports_to = str(ctx.get("reports_to", "")).lower()
        hierarchy_map = rules.get("hierarchy", {})

        def level(label):
            for k, v in hierarchy_map.items():
                if k.lower() in label:
                    return v
            return None

        report_lvl = level(reports_to)
        job_lvl = level(jb)

        if report_lvl is not None and job_lvl is not None:
            if job_lvl >= report_lvl:
                adjusted -= 0.3
            elif abs(job_lvl - report_lvl) == 1:
                adjusted += 0.05
            elif abs(job_lvl - report_lvl) >= 2:
                adjusted -= 0.1

        # === 3. Escopo ===
        scope_rules = rules.get("scope", {})
        scope_ctx = str(ctx.get("scope", "")).lower()
        for scope, titles in scope_rules.items():
            if scope.lower() == scope_ctx and any(t.lower() in jb for t in titles):
                adjusted += 0.03

        # === 4. Limite final ===
        adjusted = max(0, min(adjusted, 1.0))
        if adjusted < 0.2:
            adjusted = 0.0

    except Exception as e:
        print("Erro em adjust_similarity:", e)

    return adjusted

# ===========================================================
# 5. INTERFACE
# ===========================================================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {background-color: #f5f3f0;}
.match-card {
  background: #fff;
  border-left: 5px solid #145efc;
  border-radius: 10px;
  padding: 20px 25px;
  margin-bottom: 15px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.05);
}
.match-title {font-weight: 800; font-size: 1.1rem; color: #000;}
.match-score {color: #145efc; font-weight: 700;}
</style>
""", unsafe_allow_html=True)

st.markdown("### 🔍 Insira as informações para o Job Match")

col1, col2, col3 = st.columns(3)
with col1:
    job_desc = st.text_input("Título ou Descrição do Cargo", placeholder="Ex: HR Business Partner")
with col2:
    reports_to = st.selectbox("Reporta a", ["Diretor", "Gerente", "Coordenador", "Supervisor", "Especialista"], index=2)
with col3:
    has_team = st.selectbox("Possui equipe?", ["Não", "Sim"], index=0)

scope = st.radio("Escopo da Posição", ["Local", "Regional", "Global"], horizontal=True)
context = {"reports_to": reports_to, "has_team": has_team, "scope": scope}

if not job_desc:
    st.info("Digite o nome ou descrição de um cargo para iniciar o match.")
    st.stop()

# ===========================================================
# 6. CÁLCULO DE SIMILARIDADE
# ===========================================================
descs = df["Job Profile Description"].fillna("") + " " + df["Job Profile"].fillna("")
embeds_db = model.encode(descs.tolist(), convert_to_tensor=True)
query_embed = model.encode(job_desc, convert_to_tensor=True)
sims = util.cos_sim(query_embed, embeds_db)[0].cpu().tolist()

results = []
for i, score in enumerate(sims):
    profile = df.iloc[i]
    base_sim = float(score)
    adjusted = adjust_similarity(base_sim, job_desc, profile.get("Job Profile", ""), rules, context)
    if adjusted > 0:
        results.append({
            "Job Profile": profile.get("Job Profile", ""),
            "Job Family": profile.get("Job Family", ""),
            "Career Path": profile.get("Career Path", ""),
            "Adjusted Similarity": round(adjusted, 3)
        })

results = sorted(results, key=lambda x: x["Adjusted Similarity"], reverse=True)[:10]

# ===========================================================
# 7. RESULTADOS
# ===========================================================
st.markdown("### 📋 Resultados do Job Match")
if not results:
    st.warning("Nenhum cargo compatível foi encontrado com base nas regras hierárquicas.")
else:
    for r in results:
        st.markdown(f"""
        <div class="match-card">
            <div class="match-title">{r['Job Profile']}</div>
            <div><b>Família:</b> {r['Job Family']} | <b>Carreira:</b> {r['Career Path']}</div>
            <div class="match-score">Similaridade Ajustada: {r['Adjusted Similarity'] * 100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
