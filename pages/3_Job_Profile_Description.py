import streamlit as st
import pandas as pd
import re
import html
from pathlib import Path
from utils.ui import sidebar_logo_and_title

# ===========================================================
# 1. CONFIGURAÇÃO GERAL
# ===========================================================
st.set_page_config(
    page_title="Job Profile Description",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Carrega o CSS global
css_path = Path(__file__).parents[1] / "assets" / "header.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

sidebar_logo_and_title()

# ===========================================================
# 2. ESTILO E HEADER
# ===========================================================
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
    max-width: 1300px !important;
    padding-left: 40px !important;
    padding-right: 40px !important;
}

/* Blocos */
.profile-card {
    background: #fff;
    border-radius: 12px;
    border-left: 5px solid #145efc;
    padding: 22px 26px;
    margin-bottom: 25px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.05);
}
.profile-title {
    font-size: 1.25rem;
    font-weight: 800;
    color: #000;
    margin-bottom: 6px;
}
.profile-meta {
    font-size: 0.9rem;
    color: #666;
    margin-bottom: 12px;
}
.section-box {
    background: #fff;
    border-left: 4px solid #145efc;
    border-radius: 8px;
    padding: 18px 22px;
    margin-top: 18px;
    box-shadow: 0 3px 6px rgba(0,0,0,0.05);
}
.section-title {
    font-weight: 700;
    color: #145efc;
    font-size: 0.95rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 8px;
}
.section-content {
    color: #333;
    line-height: 1.55;
    font-size: 0.95rem;
    white-space: pre-wrap;
}
</style>

<div class="page-header">
  <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/business%20review%20clipboard.png" alt="icon">
  Job Profile Description
</div>
""", unsafe_allow_html=True)


# ===========================================================
# 3. FUNÇÕES AUXILIARES
# ===========================================================
def normalize_grade(val):
    """Remove '.0' e trata NaN"""
    s = str(val).strip()
    if s.lower() in ("nan", "none", "", "na"):
        return ""
    return re.sub(r"\.0$", "", s)


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


# ===========================================================
# 4. DADOS
# ===========================================================
df = load_excel("data/Job Profile.xlsx")
levels = load_excel("data/Structure Level.xlsx")

if df.empty:
    st.error("❌ Arquivo 'Job Profile.xlsx' não encontrado ou inválido.")
    st.stop()

df["Global Grade"] = df["Global Grade"].apply(normalize_grade)
if not levels.empty and "Global Grade" in levels.columns:
    levels["Global Grade"] = levels["Global Grade"].apply(normal
