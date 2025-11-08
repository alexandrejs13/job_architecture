import streamlit as st
import pandas as pd
from utils.data_loader import load_data
import html

# =========================
# Config da página
# =========================
st.set_page_config(page_title="Job Profile Description", layout="wide")

st.markdown("""
<style>
.main { max-width: 1800px; margin: 0 auto; padding: 1rem 2rem; }
h2, .section-title { color:#1d4ed8; }
.section-title {
    font-size: 1.2rem !important; font-weight: 700 !important;
    margin-top: 1.4rem; margin-bottom: .6rem;
}
.card {
    background:#f9fafb; border-radius: 8px; padding: 1rem 1.2rem;
    margin-bottom: .8rem; box-shadow: 0 1px 4px rgba(0,0,0,.08);
    border-left: 4px solid #2563eb; font-size:.94rem; line-height:1.5; text-align:justify;
}
.select-row .stSelectbox > div > div { font-weight:600; }
</style>
""", unsafe_allow_html=True)

# =========================
# Utilitários
# =========================
def fmt(text: str) -> str:
    """Parágrafos seguros com <br> (evita HTML bruto da planilha)."""
    if not text or str(text).strip() in {"-", "nan", "None"}:
        return "-"
    safe = html.escape(str(text))
    parts = [p.strip() for p in safe.split("\n") if p.strip()]
    return "<br>".join(parts)

def get_cell(row, cols):
    if isinstance(cols, str):
        return str(row.get(cols, "")).strip()
    for c in cols:
        if c in row and str(row[c]).strip():
            return str(row[c]).strip()
    return ""

# =========================
# Dados
# =========================
data = load_data()
if not data or "job_profile" not in data:
    st.error("Erro ao carregar 'Job Profile.csv'.")
    st.stop()

df = data["job_profile"].copy()
df.columns = [c.strip() for c in df.columns]
df = df.applymap(lambda x: str(x).strip() if isinstance(x, str) else x).fillna("")

# =========================
# Filtros
# =========================
st.markdown("## 📋 Job Profile Description")

c1, c2, c3 = st.columns([1.1, 2.5, 1.2], gap="large")
with c1:
    families = sorted(df["Job Family"].dropna().unique())
    fam = st.selectbox("Família", families)
sub_df = df[df["Job Family"].str.lower().str.strip() == fam.lower().strip()]

with c2:
    subs = sorted(sub_df["Sub Job Family"].dropna().unique())
    subfam = st.selectbox("Subfamília", subs)

with c3:
    paths = sorted(sub_df["Career Path"].dropna().unique())
    path = st.selectbox("Trilha de Carreira", paths)

view = df[
    (df["Job Family"].str.lower().str.strip() == fam.lower().strip()) &
    (df["Sub Job Family"].str.lower().str.strip() == subfam.lower().strip()) &
    (df["Career Path"].str.lower().str.strip() == path.lower().strip())
].copy()

if view.empty:
    st.warning("Nenhum cargo encontrado para os filtros.")
    st.stop()

view["__display__"] = view.apply(lambda x: f"{x['Global Grade']} — {x['Job Profile']}", axis=1)

st.markdown("<div style='margin-top:-10px'></div>", unsafe_allow_html=True)
picks = st.multiselect("Selecione até 3 cargos para comparar:", view["__display__"].tolist(), max_selections=3)
if not picks:
    st.stop()

rows = [view.loc[view["__display__"] == d].iloc[0] for d in picks]
n = len(rows)

# =========================
# Seções a exibir (títulos FORA do card)
# =========================
SECTIONS = [
    ("Sub Job Family Description", lambda r: get_cell(r, "Sub Job Family Description")),
    ("Job Profile Description",   lambda r: get_cell(r, "Job Profile Description")),
    ("Role Description",          lambda r: get_cell(r, "Role Description")),
    ("Grade Differentiator",      lambda r: get_cell(r, ["Grade Differentiator","Grade Differentiation","Grade Differentiatior"])),
    ("Qualifications",            lambda r: get_cell(r, "Qualifications")),
    ("KPIs / Specific Parameters",lambda r: get_cell(r, ["Specific parameters KPIs","Specific parameters / KPIs"])),
]

# Só mostra "Competency" se existir nas colunas
competency_cols = [c for c in df.columns if c.strip().lower().startswith("competency")]
if competency_cols:
    for i in range(1, 4):
        colname = f"Competency {i}"
        if colname in df.columns:
            SECTIONS.append((colname, lambda r, col=colname: get_cell(r, col)))

# =========================
# Renderização (SEM HTML grid; usando st.columns)
# =========================
for title, getter in SECTIONS:
    # Verifica se tem algo para exibir em pelo menos um cargo
    if not any(getter(r) and getter(r).strip() not in {"", "-", "nan", "None"} for r in rows):
        continue

    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)

    cols = st.columns(n, gap="large")
    for col, row in zip(cols, rows):
        with col:
            content = fmt(getter(row))
            st.markdown(f"<div class='card'>{content}</div>", unsafe_allow_html=True)
