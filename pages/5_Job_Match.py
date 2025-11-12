# ===========================================================
# 5_JOB_MATCH.PY — CORRIGIDO E APRIMORADO
# ===========================================================

import streamlit as st
import pandas as pd
import json
import re
from pathlib import Path
from utils.ui import sidebar_logo_and_title

# ===========================================================
# CONFIGURAÇÃO GERAL
# ===========================================================
st.set_page_config(
    page_title="Job Match",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================================================
# CSS E HEADER
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
    font-size: 1.4rem;
    border-radius: 12px;
    padding: 22px 36px;
    display: flex;
    align-items: center;
    gap: 18px;
    margin-bottom: 40px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.page-header img { width: 50px; height: 50px; }
.result-card {
    background: #fff;
    border-left: 5px solid #145efc;
    border-radius: 10px;
    padding: 18px 24px;
    margin-bottom: 18px;
    box-shadow: 0 3px 8px rgba(0,0,0,0.05);
}
.score {
    font-weight: 700;
    color: #145efc;
}
</style>

<div class="page-header">
  <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/checkmark%20success.png">
  Job Match — Alinhamento de Descrições
</div>
""", unsafe_allow_html=True)

# ===========================================================
# FUNÇÕES AUXILIARES
# ===========================================================
@st.cache_data
def load_excel(path):
    try:
        df = pd.read_excel(path)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Erro ao carregar {path}: {e}")
        return pd.DataFrame()

@st.cache_data
def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Erro ao ler {path}: {e}")
        return {}

def normalize_txt(txt):
    return re.sub(r"[^a-zA-Z0-9áéíóúãõâêôç\s]", "", str(txt)).lower().strip()

def similarity(a, b):
    a, b = normalize_txt(a), normalize_txt(b)
    if not a or not b:
        return 0
    a_set, b_set = set(a.split()), set(b.split())
    return len(a_set & b_set) / len(a_set | b_set)

# ===========================================================
# DADOS
# ===========================================================
profiles = load_excel("data/Job Profile.xlsx")
levels = load_excel("data/Level Structure.xlsx")
rules = load_json("data/job_rules.json")

if profiles.empty:
    st.error("❌ Arquivo Job Profile.xlsx não encontrado ou inválido.")
    st.stop()

# Corrigir possíveis nomes de colunas
if not levels.empty:
    levels.columns = [c.strip().lower() for c in levels.columns]
    if "level name" not in levels.columns:
        # tenta alternativas conhecidas
        rename_map = {
            "level": "level name",
            "career level": "level name",
            "nivel": "level name",
        }
        levels.rename(columns=rename_map, inplace=True)

# ===========================================================
# INTERFACE — ENTRADA DO USUÁRIO
# ===========================================================
st.subheader("🔍 Cole ou digite abaixo a descrição do cargo:")

descricao = st.text_area("Descrição do Cargo", height=280, placeholder="Cole aqui a descrição completa do cargo...")

if not descricao.strip():
    st.stop()

# ===========================================================
# ANÁLISE DE COMPATIBILIDADE
# ===========================================================
results = []
descricao_norm = normalize_txt(descricao)

for _, row in profiles.iterrows():
    nome = str(row.get("Job Profile", "")).strip()
    job_text = " ".join([
        str(row.get("Job Profile Description", "")),
        str(row.get("Role Description", "")),
        str(row.get("Grade Differentiator", "")),
        str(row.get("Qualifications", ""))
    ])
    score = similarity(descricao_norm, job_text)
    gg = str(row.get("Global Grade", "")).strip()
    fam = str(row.get("Job Family", "")).strip()
    sub = str(row.get("Sub Job Family", "")).strip()
    trilha = str(row.get("Career Path", "")).strip()

    level_name = ""
    if not levels.empty and "global grade" in levels.columns:
        match = levels[levels["global grade"].astype(str).str.strip() == gg]
        if not match.empty:
            level_name = str(match.iloc[0].get("level name", ""))

    results.append({
        "Job Profile": nome,
        "Job Family": fam,
        "Sub Job Family": sub,
        "Career Path": trilha,
        "Global Grade": gg,
        "Level Name": level_name,
        "Score": round(score, 3)
    })

df_result = pd.DataFrame(results).sort_values(by="Score", ascending=False).head(5)

# ===========================================================
# EXIBIÇÃO DOS RESULTADOS
# ===========================================================
st.header("📊 Resultados — Top 5 Matches")

if df_result.empty:
    st.warning("Nenhum resultado encontrado.")
else:
    for _, r in df_result.iterrows():
        st.markdown(f"""
        <div class="result-card">
            <div class="score">🎯 Similaridade: {r['Score']*100:.1f}%</div>
            <b>{r['Job Profile']}</b>  
            {r['Level Name']} (GG {r['Global Grade']})
            <br><b>Família:</b> {r['Job Family']}  
            <br><b>Sub-Família:</b> {r['Sub Job Family']}  
            <br><b>Trilha:</b> {r['Career Path']}
        </div>
        """, unsafe_allow_html=True)
