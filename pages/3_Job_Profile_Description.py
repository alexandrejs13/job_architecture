import streamlit as st
import pandas as pd
import re, html
from pathlib import Path
from utils.ui import sidebar_logo_and_title

st.set_page_config(page_title="Job Profile Description", page_icon="📋", layout="wide", initial_sidebar_state="expanded")

# ===========================================================
# CSS GLOBAL
# ===========================================================
css_path = Path(__file__).parents[1] / "assets" / "header.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

sidebar_logo_and_title()

# ===========================================================
# HEADER
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
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
.page-header img { width: 48px; height: 48px; }
.block-container {
    max-width: 950px !important;
    padding-left: 40px !important;
    padding-right: 40px !important;
}
[data-testid="stAppViewContainer"] {
    background-color: #f5f3f0;
    color: #202020;
    font-family: "Source Sans Pro", "Helvetica", sans-serif;
}
</style>

<div class="page-header">
    <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/business%20review%20clipboard.png" alt="icon">
    Job Profile Description
</div>
""", unsafe_allow_html=True)

# ===========================================================
# FUNÇÕES E DADOS
# ===========================================================
@st.cache_data
def load_job_profiles():
    try:
        df = pd.read_excel("data/Job Profile.xlsx")
        for c in df.select_dtypes(include="object"): df[c] = df[c].astype(str).str.strip()
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

df = load_job_profiles()

# ===========================================================
# CONTEÚDO
# ===========================================================
if not df.empty:
    families = sorted(df["Job Family"].dropna().unique())
    col1, col2, col3 = st.columns(3)
    with col1: fam = st.selectbox("Família:", families)
    with col2:
        subs = sorted(df[df["Job Family"] == fam]["Sub Job Family"].dropna().unique())
        sub = st.selectbox("Subfamília:", subs)
    with col3:
        paths = sorted(df[df["Sub Job Family"] == sub]["Career Path"].dropna().unique())
        path = st.selectbox("Trilha:", paths)

    filtered = df[(df["Job Family"] == fam) & (df["Sub Job Family"] == sub) & (df["Career Path"] == path)]

    profiles = sorted(filtered["Job Profile"].unique())
    selected = st.multiselect("Selecione até 3 perfis:", profiles, max_selections=3)

    if selected:
        cols = len(selected)
        st.markdown(f'<div style="display:grid;grid-template-columns:repeat({cols},1fr);gap:25px;">', unsafe_allow_html=True)

        for s in selected:
            item = filtered[filtered["Job Profile"] == s].iloc[0]
            st.markdown(f"""
            <div style="background:white;border-left:5px solid #145efc;padding:20px;border-radius:10px;box-shadow:0 4px 8px rgba(0,0,0,0.05);">
                <h4 style="color:#145efc;margin-bottom:8px;">{item['Job Profile']}</h4>
                <p><b>Global Grade:</b> {item.get('Global Grade','-')}</p>
                <p><b>Descrição:</b><br>{item.get('Job Profile Description','-')}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Selecione até 3 cargos para comparar.")
else:
    st.warning("Base de dados não encontrada.")
