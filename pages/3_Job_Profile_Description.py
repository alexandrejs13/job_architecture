# pages/3_Job_Profile_Description.py
import streamlit as st
import pandas as pd
import re
import html as html_lib
from pathlib import Path
import streamlit.components.v1 as components
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
# 2. CSS LOCAL
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
.comparison-grid { display: grid; gap: 20px; margin-top: 20px; }
.grid-cell { background: #fff; border: 1px solid #e0e0e0; padding: 15px; display: flex; flex-direction: column; }
.header-cell { background: #f8f9fa; border-radius: 12px 12px 0 0; border-bottom: none; }
.fjc-title { font-size: 18px; font-weight: 800; color: #2c3e50; margin-bottom: 10px; min-height: 50px; }
.fjc-gg-row { display: flex; justify-content: space-between; align-items: center; }
.fjc-gg { color: #145efc; font-weight: 700; }
.meta-cell { border-top: 1px solid #eee; border-bottom: 1px solid #eee; font-size: 0.9rem; color: #555; min-height: 120px; }
.meta-row { margin-bottom: 6px; }
.section-cell { border-left-width: 5px; border-left-style: solid; border-top: none; background: #fdfdfd; }
.section-title { font-weight: 700; font-size: 0.95rem; margin-bottom: 8px; color: #333; display: flex; align-items: center; gap: 6px; }
.section-content { color: #444; font-size: 0.9rem; line-height: 1.5; white-space: pre-wrap; }
.footer-cell { height: 10px; border-top: none; border-radius: 0 0 12px 12px; background: #fff; }
</style>

<div class="page-header">
  <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/business%20review%20clipboard.png" alt="icon">
  Job Profile Description
</div>
""", unsafe_allow_html=True)


# ===========================================================
# 3. FUNÇÕES AUXILIARES
# ===========================================================
def normalize_grade(val: object) -> str:
    """Remove '.0' e trata NaN."""
    s = str(val).strip()
    if s.lower() in ("nan", "none", "", "na"):
        return ""
    s = re.sub(r"\.0$", "", s)
    return s


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
# 6. RENDERIZAÇÃO GRID LADO A LADO
# ===========================================================
cards = []
for name in selected:
    item = filtered[filtered["Job Profile"] == name]
    if item.empty:
        continue
    row = item.iloc[0].copy()

    gg_val = normalize_grade(row.get("Global Grade", ""))
    lvl_name = ""
    if not df_levels.empty and {"Global Grade", "Level Name"}.issubset(df_levels.columns):
        match = df_levels[df_levels["Global Grade"].astype(str).str.strip() == gg_val]
        if not match.empty:
            lvl_name = f" • {match['Level Name'].iloc[0]}"

    gg_display = gg_val if gg_val else "-"
    cards.append({"row": row, "lvl": lvl_name, "gg": gg_display})

if not cards:
    st.warning("Não foi possível montar a comparação para os itens selecionados.")
    st.stop()

cols = len(cards)
html_parts = [f'<div class="comparison-grid" style="grid-template-columns:repeat({cols},1fr);">']

# Cabeçalho
for c in cards:
    r = c["row"]
    html_parts.append(f"""
    <div class="grid-cell header-cell">
      <div class="fjc-title">{html_lib.escape(str(r.get('Job Profile','-')))}</div>
      <div class="fjc-gg-row">
        <div class="fjc-gg">GG {html_lib.escape(c['gg'])}{html_lib.escape(c['lvl'])}</div>
        <div style="font-weight:700; color:#145efc;">Comparação</div>
      </div>
    </div>
    """)

# Metadados
for c in cards:
    r = c["row"]
    html_parts.append(f"""
    <div class="grid-cell meta-cell">
      <div class="meta-row"><strong>Família:</strong> {html_lib.escape(str(r.get('Job Family','-')))}</div>
      <div class="meta-row"><strong>Subfamília:</strong> {html_lib.escape(str(r.get('Sub Job Family','-')))}</div>
      <div class="meta-row"><strong>Carreira:</strong> {html_lib.escape(str(r.get('Career Path','-')))}</div>
      <div class="meta-row"><strong>Cód:</strong> {html_lib.escape(str(r.get('Full Job Code','-')))}</div>
    </div>
    """)

# Seções
sections_config = [
    ("🧭 Sub Job Family Description", "Sub Job Family Description", "#95a5a6"),
    ("🧠 Job Profile Description",   "Job Profile Description",   "#e91e63"),
    ("🏛️ Career Band Description",   "Career Band Description",   "#673ab7"),
    ("🎯 Role Description",          "Role Description",          "#145efc"),
    ("🏅 Grade Differentiator",      "Grade Differentiator",      "#ff9800"),
    ("🎓 Qualifications",            "Qualifications",            "#009688"),
]

for title, field, color in sections_config:
    for c in cards:
        content = str(c["row"].get(field, "") or "").strip()
        if field == "Qualifications" and len(content) < 2:
            html_parts.append('<div class="grid-cell section-cell" style="border-left-color: transparent; background: transparent; border: none;"></div>')
        else:
            html_parts.append(f"""
            <div class="grid-cell section-cell" style="border-left-color:{color};">
              <div class="section-title" style="color:{color};">{title}</div>
              <div class="section-content">{html_lib.escape(content)}</div>
            </div>
            """)

for _ in cards:
    html_parts.append('<div class="grid-cell footer-cell"></div>')

html_parts.append('</div>')

components.html("\n".join(html_parts), height=1000, scrolling=True)
