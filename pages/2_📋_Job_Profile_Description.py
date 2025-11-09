import re
import streamlit as st
import pandas as pd
from utils.ui_components import section

st.set_page_config(layout="wide")

# ===========================================================
# CSS — layout mantido idêntico ao modelo anterior
# ===========================================================
st.markdown("""
<style>
.block-container {
  max-width: 1200px !important;
  min-width: 900px !important;
  margin: 0 auto !important;
  padding: 2.5rem 1.5rem 2rem 1.5rem;
  zoom: 0.9;
}
html, body, [class*="css"] {
  font-size: calc(13px + 0.18vw) !important;
}
h1 { text-align: left !important; margin-top: 0.8rem !important; margin-bottom: 1.4rem !important; font-size: 1.9rem !important; }
.ja-p { margin: 0 0 4px 0; text-align: left; line-height: 1.48; }
.ja-hd { display:flex; flex-direction:column; align-items:flex-start; gap:4px; margin:0 0 6px 0; text-align:left; }
.ja-hd-title { font-size:1.15rem; font-weight:700; }
.ja-hd-grade { color:#1E56E0; font-weight:700; font-size:1rem; }
.ja-class { background:#fff; border:1px solid #e0e4f0; border-radius:6px; padding:8px 12px; width:100%; text-align:left; min-height:130px; }
.ja-sec-h { display:flex; align-items:center; gap:6px; margin:0 0 3px 0 !important; }
.ja-ic { width:18px; text-align:center; }
.ja-ttl { font-weight:700; color:#1E56E0; font-size:0.95rem; }
.ja-card { background:#f9f9f9; padding:10px 14px; border-radius:6px; border-left:3px solid #1E56E0; min-height:120px; }
.ja-grid { display:grid; gap:14px; margin:6px 0 12px 0 !important; }
.ja-grid.cols-1 { grid-template-columns: repeat(1, 1fr); }
.ja-grid.cols-2 { grid-template-columns: repeat(2, 1fr); }
.ja-grid.cols-3 { grid-template-columns: repeat(3, 1fr); }
</style>
""", unsafe_allow_html=True)

# ===========================================================
# Carregar Excel
# ===========================================================
@st.cache_data
def load_job_data():
    path = "data/Job Family.xlsx"
    df = pd.read_excel(path)
    df.columns = [c.strip() for c in df.columns]
    return df

df = load_job_data()

section("📘 Job Profile Description")

# ===========================================================
# Verificação de colunas
# ===========================================================
required = [
    "Job Profile", "Sub Job Family Description", "Job Profile Description",
    "Career Band Description", "Role Description", "Grade Differentiator", "Qualifications",
    "Job Family", "Sub Job Family", "Career Path", "Function Code", "Discipline Code", "Global Grade", "Full Job Code"
]
missing = [c for c in required if c not in df.columns]
if missing:
    st.error(f"As seguintes colunas estão faltando: {', '.join(missing)}")
    st.stop()

# ===========================================================
# Filtros
# ===========================================================
col1, col2, col3 = st.columns([1.2, 2.2, 1])
with col1:
    families = sorted(df["Job Family"].dropna().unique())
    fam = st.selectbox("Família", families)
filtered = df[df["Job Family"] == fam]

with col2:
    subs = sorted(filtered["Sub Job Family"].dropna().unique())
    sub = st.selectbox("Subfamília", subs)
sub_df = filtered[filtered["Sub Job Family"] == sub]

with col3:
    careers = sorted(sub_df["Career Path"].dropna().unique())
    career = st.selectbox("Trilha de Carreira", careers)
career_df = sub_df[sub_df["Career Path"] == career]

# ===========================================================
# Multiselect de cargos
# ===========================================================
def option_label(row):
    g = row.get("Global Grade", "")
    p = row.get("Job Profile", "")
    return f"GG{int(g)} — {p}" if str(g).isdigit() else p

career_df_sorted = career_df.sort_values(by="Global Grade", ascending=False)
pick_options = career_df_sorted.apply(option_label, axis=1).tolist()

st.markdown('<div class="compare-box"><b>Selecione até 3 cargos para comparar:</b></div>', unsafe_allow_html=True)
selected_labels = st.multiselect("", options=pick_options, max_selections=3, label_visibility="collapsed")

# ===========================================================
# Renderização
# ===========================================================
if selected_labels:
    st.markdown("---")
    st.markdown("### 🧾 Comparativo de Cargos Selecionados")

    rows = []
    for label in selected_labels:
        parts = re.split(r"\s*[–—-]\s*", label)
        grade = parts[0].replace("GG", "").strip() if parts else ""
        title = parts[1].strip() if len(parts) > 1 else label.strip()
        sel = career_df_sorted[career_df_sorted["Job Profile"].str.strip().str.lower() == title.lower()]
        if grade:
            sel = sel[sel["Global Grade"].astype(str).str.strip() == grade]
        rows.append(sel.iloc[0] if not sel.empty else None)

    n = len(rows)
    grid_class = f"ja-grid cols-{n}"

    def safe(row, col): return str(row[col]).strip() if row is not None and col in row and str(row[col]).strip() else "-"

    # Cabeçalhos
    html_cells = [
        f"<div class='ja-hd'><div class='ja-hd-title'>{safe(r, 'Job Profile')}</div><div class='ja-hd-grade'>GG {safe(r, 'Global Grade')}</div></div>"
        for r in rows
    ]
    st.markdown(f"<div class='{grid_class}'>" + "".join(html_cells) + "</div>", unsafe_allow_html=True)

    # Box de informações
    html_cells = [
        f"<div class='ja-class'><b>Família:</b> {safe(r, 'Job Family')}<br>"
        f"<b>Subfamília:</b> {safe(r, 'Sub Job Family')}<br>"
        f"<b>Carreira:</b> {safe(r, 'Career Path')}<br>"
        f"<b>Função:</b> {safe(r, 'Function Code')}<br>"
        f"<b>Disciplina:</b> {safe(r, 'Discipline Code')}<br>"
        f"<b>Código:</b> {safe(r, 'Full Job Code')}</div>"
        for r in rows
    ]
    st.markdown(f"<div class='{grid_class}'>" + "".join(html_cells) + "</div>", unsafe_allow_html=True)

    # Seções
    SECTIONS = [
        ("🧭", "Sub Job Family Description"),
        ("🧠", "Job Profile Description"),
        ("🎓", "Career Band Description"),
        ("🎯", "Role Description"),
        ("🏅", "Grade Differentiator"),
        ("📘", "Qualifications"),
    ]

    for emoji, title in SECTIONS:
        html_cells = [
            f"<div><div class='ja-sec-h'><span class='ja-ic'>{emoji}</span><span class='ja-ttl'>{title}</span></div><div class='ja-card'>{safe(r, title)}</div></div>"
            for r in rows
        ]
        st.markdown(f"<div class='{grid_class}'>" + "".join(html_cells) + "</div>", unsafe_allow_html=True)
