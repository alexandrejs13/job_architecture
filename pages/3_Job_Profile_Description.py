import streamlit as st
import pandas as pd
import re
import html as html_lib
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

css_path = Path(__file__).parents[1] / "assets" / "header.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

sidebar_logo_and_title()


# ===========================================================
# 2. CSS LOCAL (mantendo visual anterior)
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
.block-container {
    max-width: 950px !important;
    padding-left: 40px !important;
    padding-right: 40px !important;
}
[data-testid="stAppViewContainer"] {
    background-color: #f5f3f0;
    color: #202020;
    font-family: "Source Sans Pro","Helvetica",sans-serif;
}
.section-box {
    background-color: #ffffff;
    border-left: 5px solid #145efc;
    padding: 25px;
    border-radius: 8px;
    margin-top: 20px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}
.section-title {
    font-weight: 700;
    color: #145efc;
    font-size: 1rem;
    margin-bottom: 8px;
}
.section-content {
    color: #333333;
    font-size: 0.95rem;
    line-height: 1.6;
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
def load_job_profiles():
    try:
        df = pd.read_excel("data/Job Profile.xlsx")
        for c in df.select_dtypes(include="object"):
            df[c] = df[c].astype(str).str.strip()
        return df
    except Exception as e:
        st.error(f"Erro ao carregar Job Profile.xlsx: {e}")
        return pd.DataFrame()


@st.cache_data
def load_levels():
    try:
        lv = pd.read_excel("data/Structure Level.xlsx")
        for c in lv.select_dtypes(include="object"):
            lv[c] = lv[c].astype(str).str.strip()
        return lv
    except Exception:
        return pd.DataFrame()


# ===========================================================
# 4. DADOS
# ===========================================================
df = load_job_profiles()
df_levels = load_levels()

if df.empty:
    st.error("❌ Não foi possível carregar o arquivo Job Profile.xlsx.")
    st.stop()

df["Global Grade"] = df["Global Grade"].apply(normalize_grade)
if not df_levels.empty and "Global Grade" in df_levels.columns:
    df_levels["Global Grade"] = df_levels["Global Grade"].apply(normalize_grade)


# ===========================================================
# 5. FILTROS
# ===========================================================
families = sorted(x for x in df["Job Family"].dropna().unique() if x)
col1, col2, col3 = st.columns(3)

with col1:
    fam = st.selectbox("Família:", ["Selecione..."] + families, index=0)
with col2:
    subs = sorted(df[df["Job Family"] == fam]["Sub Job Family"].dropna().unique()) if fam != "Selecione..." else []
    sub = st.selectbox("Subfamília:", ["Selecione..."] + subs, index=0)
with col3:
    paths = sorted(df[df["Sub Job Family"] == sub]["Career Path"].dropna().unique()) if sub != "Selecione..." else []
    path = st.selectbox("Trilha (Career Path):", ["Selecione..."] + paths, index=0)

filtered = df.copy()
if fam != "Selecione...":
    filtered = filtered[filtered["Job Family"] == fam]
if sub != "Selecione...":
    filtered = filtered[filtered["Sub Job Family"] == sub]
if path != "Selecione...":
    filtered = filtered[filtered["Career Path"] == path]

if filtered.empty:
    st.info("Ajuste os filtros para visualizar os perfis.")
    st.stop()

profiles = sorted(filtered["Job Profile"].dropna().unique())
selected = st.multiselect("Selecione até 3 perfis para comparar:", profiles, max_selections=3)

if not selected:
    st.info("Selecione até 3 cargos para comparar.")
    st.stop()


# ===========================================================
# 6. VISUALIZAÇÃO (mantém formatação anterior e mostra GG)
# ===========================================================
cols = st.columns(len(selected))

for idx, name in enumerate(selected):
    item = filtered[filtered["Job Profile"] == name]
    if item.empty:
        continue

    row = item.iloc[0].copy()
    gg = normalize_grade(row.get("Global Grade", ""))
    lvl_name = ""

    if not df_levels.empty and {"Global Grade", "Level Name"}.issubset(df_levels.columns):
        match = df_levels[df_levels["Global Grade"].astype(str).str.strip() == gg]
        if not match.empty:
            lvl_name = match["Level Name"].iloc[0]

    with cols[idx]:
        st.markdown(f"### {row.get('Job Profile', '-')}")
        st.caption(f"GG {gg or '-'} • {lvl_name}")
        st.divider()

        sections = [
            ("🧭 Sub Job Family Description", "Sub Job Family Description"),
            ("🧠 Job Profile Description", "Job Profile Description"),
            ("🏛️ Career Band Description", "Career Band Description"),
            ("🎯 Role Description", "Role Description"),
            ("🏅 Grade Differentiator", "Grade Differentiator"),
            ("🎓 Qualifications", "Qualifications")
        ]

        for title, field in sections:
            content = str(row.get(field, "") or "").strip()
            if not content:
                continue
            st.markdown(f"""
            <div class="section-box">
                <div class="section-title">{title}</div>
                <div class="section-content">{html_lib.escape(content)}</div>
            </div>
            """, unsafe_allow_html=True)
