import streamlit as st
import pandas as pd
from utils.data_loader import load_data
import html

# ================================================
# Configurações gerais
# ================================================
st.set_page_config(page_title="Job Profile Description", layout="wide")

st.markdown("""
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
    font-size: 1.2rem !important;
    font-weight: 700 !important;
    color: #1d4ed8;
    margin-top: 1.4rem;
    margin-bottom: 0.6rem;
    text-align: left;
}
.card {
    background: #f9fafb;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    box-shadow: 0px 1px 4px rgba(0,0,0,0.08);
    border-left: 4px solid #2563eb;
    font-size: 0.94rem;
    line-height: 1.5;
    text-align: justify;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    height: 100%;
}
.grid-container {
    display: grid;
    gap: 1.2rem;
    align-items: stretch;
}
.grid-1 { grid-template-columns: 1fr; }
.grid-2 { grid-template-columns: 1fr 1fr; }
.grid-3 { grid-template-columns: 1fr 1fr 1fr; }
</style>
""", unsafe_allow_html=True)

# ================================================
# Carregamento dos dados
# ================================================
data = load_data()
if not data or "job_profile" not in data:
    st.error("Erro: arquivo 'Job Profile.csv' não encontrado ou com erro.")
    st.stop()

df = data["job_profile"].copy()
df.columns = [c.strip() for c in df.columns]
df = df.applymap(lambda x: str(x).strip() if isinstance(x, str) else x)
df.fillna("", inplace=True)

# ================================================
# Filtros superiores
# ================================================
st.markdown("## 📋 Job Profile Description")

col1, col2, col3 = st.columns([1.1, 2.5, 1.2])

families = sorted(df["Job Family"].dropna().unique())
selected_family = col1.selectbox("Família", families)

filtered_sub = df[df["Job Family"].str.lower().str.strip() == selected_family.lower().strip()]
sub_families = sorted(filtered_sub["Sub Job Family"].dropna().unique())
selected_subfamily = col2.selectbox("Subfamília", sub_families)

paths = sorted(filtered_sub["Career Path"].dropna().unique())
selected_path = col3.selectbox("Trilha de Carreira", paths)

career_df_sorted = df[
    (df["Job Family"].str.lower().str.strip() == selected_family.lower().strip()) &
    (df["Sub Job Family"].str.lower().str.strip() == selected_subfamily.lower().strip()) &
    (df["Career Path"].str.lower().str.strip() == selected_path.lower().strip())
]

# ================================================
# Seleção de cargos
# ================================================
if career_df_sorted.empty:
    st.warning("Nenhum cargo encontrado para os filtros selecionados.")
    st.stop()

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
# Funções utilitárias
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
    safe = html.escape(str(text))
    parts = [p.strip() for p in safe.split("\n") if p.strip()]
    return "<br>".join(parts)

# ================================================
# Estrutura das seções
# ================================================
SECTIONS = [
    ("Sub Job Family Description", lambda r: safe_get(r, "Sub Job Family Description")),
    ("Job Profile Description",   lambda r: safe_get(r, "Job Profile Description")),
    ("Role Description",          lambda r: safe_get(r, "Role Description")),
    ("Grade Differentiator",      lambda r: safe_get(r, [
        "Grade Differentiator", "Grade Differentiation", "Grade Differentiatior"
    ])),
    ("Qualifications",            lambda r: safe_get(r, "Qualifications")),
    ("KPIs / Specific Parameters", lambda r: safe_get(r, [
        "Specific parameters KPIs", "Specific parameters / KPIs"
    ])),
]

competency_cols = [c for c in career_df_sorted.columns if c.strip().lower().startswith("competency")]
if competency_cols:
    SECTIONS.extend([
        ("Competency 1", lambda r: safe_get(r, "Competency 1")),
        ("Competency 2", lambda r: safe_get(r, "Competency 2")),
        ("Competency 3", lambda r: safe_get(r, "Competency 3")),
    ])

# ================================================
# Renderização — títulos fora dos cards + cargos lado a lado
# ================================================
for title, getter in SECTIONS:
    has_content = any(
        getter(r) and getter(r).strip() not in ["", "-", "nan", "NaN", "None"]
        for r in rows if r is not None
    )
    if not has_content:
        continue

    # título da seção
    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)

    # define a quantidade de colunas conforme número de cargos
    grid_class = f"grid-container grid-{len(rows)}"

    # monta o HTML de todos os cards em um único bloco
    html_cards = ""
    for r in rows:
        raw = getter(r)
        html_cards += f"""
        <div class='card'>
            <div>{format_paragraphs(raw)}</div>
        </div>
        """

    # renderiza o grid completo em um único markdown
    st.markdown(f"<div class='{grid_class}'>{html_cards}</div>", unsafe_allow_html=True)
