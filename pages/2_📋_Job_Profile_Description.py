import streamlit as st
import pandas as pd
from utils.data_loader import load_data

# ================================================
# 🔧 Configurações iniciais
# ================================================
st.set_page_config(page_title="Job Profile Description", layout="wide")

st.markdown(
    """
    <style>
    .main {
        max-width: 1800px;
        margin: 0 auto;
        padding: 1rem 2rem;
    }
    .stSelectbox label, .stMultiSelect label {
        font-weight: 600 !important;
        color: #333;
    }
    .section-title {
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        color: #1d4ed8;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
    }
    .card {
        background: #f9fafb;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.6rem;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.08);
        border-left: 4px solid #2563eb;
        line-height: 1.5;
        font-size: 0.95rem;
    }
    .title-icon {
        font-size: 1.1rem;
        margin-right: 0.4rem;
    }
    .grid-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.2rem;
        align-items: start;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ================================================
# 🧭 Carregamento de dados
# ================================================
data = load_data()
if not data or "job_profile" not in data:
    st.error("Erro: arquivo 'Job Profile.csv' não encontrado ou com erro.")
    st.stop()

df = data["job_profile"].copy()

# Normaliza colunas
df.columns = [c.strip() for c in df.columns]
df.fillna("", inplace=True)

# ================================================
# 🧱 Layout: filtros superiores
# ================================================
st.markdown("## 📋 Job Profile Description")

col1, col2, col3 = st.columns([1.1, 2.5, 1.2])

with col1:
    families = sorted(df["Job Family"].dropna().unique())
    selected_family = st.selectbox("Família", families)

with col2:
    filtered_sub = df[df["Job Family"] == selected_family]
    sub_families = sorted(filtered_sub["Sub Job Family"].dropna().unique())
    selected_subfamily = st.selectbox("Subfamília", sub_families)

with col3:
    paths = sorted(df["Career Path"].dropna().unique())
    selected_path = st.selectbox("Trilha de Carreira", paths)

career_df_sorted = df[
    (df["Job Family"] == selected_family)
    & (df["Sub Job Family"] == selected_subfamily)
    & (df["Career Path"] == selected_path)
]

# ================================================
# 🎯 Seleção de cargos
# ================================================
career_df_sorted["Display"] = career_df_sorted.apply(
    lambda x: f"{x['Global Grade']} — {x['Job Profile']}", axis=1
)
st.markdown("<div style='margin-top:-10px'></div>", unsafe_allow_html=True)
selected_roles = st.multiselect(
    "Selecione até 3 cargos para comparar:",
    options=career_df_sorted["Display"].tolist(),
    max_selections=3,
)

if not selected_roles:
    st.stop()

rows = [
    career_df_sorted.loc[career_df_sorted["Display"] == role].iloc[0]
    for role in selected_roles
]

# ================================================
# 🧩 Funções utilitárias
# ================================================
def safe_get(row, cols):
    if isinstance(cols, str):
        return str(row.get(cols, "")).strip()
    for c in cols:
        if c in row and str(row[c]).strip():
            return str(row[c]).strip()
    return ""

def format_paragraphs(text):
    if not text or str(text).strip() in ["-", "nan", "None"]:
        return "-"
    parts = [p.strip() for p in str(text).split("\n") if p.strip()]
    return "<br>".join(parts)

def cell_card(icon, title, body):
    return f"""
    <div class='card'>
        <div class='section-title'><span class='title-icon'>{icon}</span>{title}</div>
        <div>{body}</div>
    </div>
    """

grid_class = "grid-container"

# ================================================
# 🧱 Renderização das seções comparativas
# ================================================
SECTIONS = [
    ("🧭", "Sub Job Family Description", lambda r: safe_get(r, "Sub Job Family Description")),
    ("🧠", "Job Profile Description",   lambda r: safe_get(r, "Job Profile Description")),
    ("🎯", "Role Description",          lambda r: safe_get(r, "Role Description")),
    ("🏅", "Grade Differentiator",      lambda r: safe_get(r, [
        "Grade Differentiator",
        "Grade Differentiation",
        "Grade Differentiatior",
    ])),
    ("📊", "KPIs / Specific Parameters", lambda r: safe_get(r, [
        "Specific parameters KPIs",
        "Specific parameters / KPIs"
    ])),
    ("🎓", "Qualifications",            lambda r: safe_get(r, "Qualifications")),
]

# 🔹 Adiciona Competencies dinamicamente, apenas se existirem
competency_cols = [c for c in career_df_sorted.columns if c.strip().lower().startswith("competency")]
if competency_cols:
    SECTIONS.extend([
        ("💡", "Competency 1", lambda r: safe_get(r, "Competency 1")),
        ("💡", "Competency 2", lambda r: safe_get(r, "Competency 2")),
        ("💡", "Competency 3", lambda r: safe_get(r, "Competency 3")),
    ])

# ================================================
# 🔍 Exibe seções com dados válidos
# ================================================
for emoji, title, getter in SECTIONS:
    has_content = any(
        getter(r) and getter(r).strip() not in ["", "-", "nan", "NaN", "None"]
        for r in rows if r is not None
    )
    if not has_content:
        continue

    html_cells = []
    for r in rows:
        raw = getter(r)
        html_cells.append("<div>" + cell_card(emoji, title, format_paragraphs(raw)) + "</div>")

    st.markdown(f"<div class='{grid_class}'>" + "".join(html_cells) + "</div>", unsafe_allow_html=True)
