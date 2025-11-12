import streamlit as st
import pandas as pd
import json
import re
from pathlib import Path
from utils.ui import sidebar_logo_and_title

# ===========================================================
# 1. CONFIGURAÇÃO GERAL
# ===========================================================
st.set_page_config(
    page_title="Job Match",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================================================
# 2. CSS GLOBAL E SIDEBAR
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
.page-header img { width: 50px; height: 50px; }
[data-testid="stAppViewContainer"] {
    background-color: #f5f3f0;
    color: #202020;
    font-family: "Source Sans Pro", "Helvetica", sans-serif;
}
.result-card {
    background: #fff;
    border-left: 5px solid #145efc;
    border-radius: 10px;
    padding: 18px 24px;
    margin-bottom: 18px;
    box-shadow: 0 3px 8px rgba(0,0,0,0.05);
}
.result-title {
    font-weight: 750;
    font-size: 1.1rem;
    color: #000;
}
.result-sub {
    color: #444;
    font-size: 0.9rem;
    margin-bottom: 6px;
}
</style>
<div class="page-header">
  <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/checkmark%20success.png" alt="icon">
  Job Match — Inteligência de Correlação
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 3. FUNÇÕES AUXILIARES
# ===========================================================
@st.cache_data
def load_file(path):
    try:
        if path.endswith(".json"):
            with open(path, "r") as f:
                return json.load(f)
        if path.endswith(".xlsx"):
            return pd.read_excel(path)
        return None
    except Exception as e:
        st.error(f"Erro ao carregar {path}: {e}")
        return None

def normalize_text(txt):
    return re.sub(r"[^a-z0-9 ]+", " ", str(txt).lower()).strip()

def grade_to_level(grade, levels_df):
    """Retorna nome de nível conforme 'Level Name', 'Level' ou 'Career Level Name'."""
    g = str(grade).strip()
    if levels_df is None or levels_df.empty:
        return ""
    cols = list(levels_df.columns)
    name_col = next((c for c in ["Level Name", "Career Level Name", "Level"] if c in cols), None)
    if not name_col:
        return ""
    match = levels_df[levels_df["Global Grade"].astype(str).str.strip() == g]
    if not match.empty:
        return str(match[name_col].iloc[0])
    return ""

def compute_match_score(text, rule_set):
    text = normalize_text(text)
    score = 0
    weights = rule_set["rules"]["matching_weights"]

    # Palavras-chave básicas
    if any(k in text for k in ["lidera", "coordena", "supervisiona"]):
        score += 0.2
    if any(k in text for k in ["analisa", "apoia", "executa"]):
        score += 0.1
    if any(k in text for k in ["estratégia", "planejamento", "gestão"]):
        score += 0.2

    # Penaliza inconsistências (ex: menciona “apoia” + “gerente”)
    if "apoia" in text and "gerente" in text:
        score -= 0.15

    return max(0, min(1, score))

# ===========================================================
# 4. DADOS
# ===========================================================
rules = load_file("data/job_rules.json")
profiles = load_file("data/Job Profile.xlsx")
levels = load_file("data/Level Structure.xlsx")

if profiles is None or profiles.empty:
    st.error("❌ Arquivo 'Job Profile.xlsx' não encontrado.")
    st.stop()

# ===========================================================
# 5. INTERFACE DE ENTRADA
# ===========================================================
st.markdown("### 🧩 Descrição do Cargo para Análise")
desc_input = st.text_area("Cole aqui a descrição completa do cargo:", height=260, placeholder="Exemplo: Responsável por prestar suporte nas atividades de RH...")

if not desc_input.strip():
    st.info("Insira uma descrição para iniciar o Job Match.")
    st.stop()

# ===========================================================
# 6. ANÁLISE
# ===========================================================
st.markdown("### ⚙️ Processando correspondências...")

profiles["normalized"] = profiles["Job Profile Description"].fillna("").apply(normalize_text)
text_input = normalize_text(desc_input)

matches = []
for _, row in profiles.iterrows():
    desc = row.get("Job Profile Description", "")
    sim = compute_match_score(desc + " " + text_input, rules)
    lvl_name = grade_to_level(row.get("Global Grade", ""), levels)
    matches.append({
        "Job Profile": row.get("Job Profile", ""),
        "Global Grade": row.get("Global Grade", ""),
        "Level Name": lvl_name,
        "Similarity": sim
    })

df_results = pd.DataFrame(matches).sort_values("Similarity", ascending=False).head(10)

# ===========================================================
# 7. EXIBIÇÃO
# ===========================================================
for _, r in df_results.iterrows():
    color = "#145efc" if r["Similarity"] > 0.8 else "#f5a623" if r["Similarity"] > 0.6 else "#bbb"
    st.markdown(f"""
    <div class="result-card" style="border-left-color:{color}">
        <div class="result-title">{r['Job Profile']}</div>
        <div class="result-sub">GG {r['Global Grade']} • {r['Level Name']}</div>
        <div>🎯 Similaridade: <b>{r['Similarity']*100:.1f}%</b></div>
    </div>
    """, unsafe_allow_html=True)
