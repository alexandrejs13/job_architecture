import streamlit as st
import pandas as pd
import random
from utils.data_loader import load_excel_data
from utils.ui_components import section, lock_sidebar

# ===========================================================
# CONFIGURAÇÃO DA PÁGINA
# ===========================================================
st.set_page_config(layout="wide", page_title="🗺️ Job Map")
lock_sidebar()
section("🗺️ Job Map")

# ===========================================================
# CSS
# ===========================================================
st.markdown("""
<style>
.block-container {
  max-width: 1700px !important;
  min-width: 1500px !important;
  margin: 0 auto !important;
}
h1 {
  color: #145efc !important;
  font-weight: 800 !important;
  font-size: 1.9rem !important;
  margin-bottom: 1rem !important;
  display: flex; align-items: center; gap: 8px;
}

/* ======= ÁREA DE SCROLL ======= */
.map-wrapper {
  overflow-x: auto;
  overflow-y: auto;
  border-top: 3px solid #145efc;
  border-bottom: 3px solid #145efc;
  background: #fff;
  padding-bottom: 1rem;
  white-space: nowrap;
}

/* ======= GRID PRINCIPAL ======= */
.jobmap-grid {
  display: grid;
  border-collapse: collapse;
  font-size: 0.85rem;
  text-align: center;
  width: max-content;
  position: relative;
}
.jobmap-grid > div {
  border: 1px solid #e0e0e0;
  box-sizing: border-box;
}

/* ======= CABEÇALHOS ======= */
.header-family {
  font-weight: 800;
  color: #fff;
  padding: 10px;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}
.header-subfamily {
  font-weight: 600;
  background: #f0f2ff;
  padding: 8px 10px;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  word-wrap: break-word;
  white-space: normal;
  line-height: 1.2;
}

/* ======= COLUNA GG FIXA ======= */
.grade-header {
  font-weight: 800;
  font-size: 1rem;
  background: #000;
  color: #fff;
  padding: 12px 10px;
  position: sticky;
  top: 0;
  left: 0;
  z-index: 50 !important;
}
.grade-cell {
  font-weight: 700;
  background: #000;
  color: #fff;
  padding: 8px;
  position: sticky;
  left: 0;
  z-index: 40 !important;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ======= CÉLULAS DE CARGO ======= */
.job-card {
  background: #fafafa;
  border-left: 4px solid #145efc;
  border-radius: 6px;
  padding: 6px 10px;
  margin: 4px 4px;
  text-align: left;
  font-size: 0.82rem;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
  white-space: normal;
}
.job-card span {
  display: block;
  font-size: 0.75rem;
  color: #555;
}
.job-card:hover {
  background: #eef3ff;
}

/* ======= ZEBRA ======= */
.grade-row:nth-child(even) {
  background: #fcfcfc;
}

/* ======= CABEÇALHOS FIXOS ======= */
.sticky-header {
  position: sticky;
  top: 0;
  z-index: 45 !important;
}
.sticky-subheader {
  position: sticky;
  top: 42px;
  z-index: 44 !important;
}

/* ======= RESPONSIVIDADE ======= */
@media (max-width: 1500px) { .block-container { zoom: 0.9; } }
@media (max-width: 1200px) { .block-container { zoom: 0.8; } }
</style>
""", unsafe_allow_html=True)

# ===========================================================
# DADOS
# ===========================================================
data = load_excel_data()
df = data.get("job_profile", pd.DataFrame())

required_cols = ["Job Family", "Sub Job Family", "Job Profile", "Career Path", "Global Grade", "Full Job Code"]
missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error(f"Colunas ausentes no Excel: {', '.join(missing)}")
    st.stop()

df = df.dropna(subset=["Job Family", "Sub Job Family", "Job Profile", "Global Grade"])
df["Global Grade"] = df["Global Grade"].astype(str).str.replace(r"\\.0$", "", regex=True)

# ===========================================================
# FILTROS
# ===========================================================
col1, col2 = st.columns([2, 2])
with col1:
    fam_opts = ["Todas"] + sorted(df["Job Family"].dropna().unique().tolist())
    selected_family = st.selectbox("Família", fam_opts)
with col2:
    path_opts = ["Todas"] + sorted(df["Career Path"].dropna().unique().tolist())
    selected_path = st.selectbox("Trilha de Carreira", path_opts)

filtered = df.copy()
if selected_family != "Todas":
    filtered = filtered[filtered["Job Family"] == selected_family]
if selected_path != "Todas":
    filtered = filtered[filtered["Career Path"] == selected_path]

if filtered.empty:
    st.warning("Nenhum cargo encontrado com os filtros selecionados.")
    st.stop()

# ===========================================================
# CORES — FAMÍLIAS E SUBFAMÍLIAS
# ===========================================================
families = sorted(filtered["Job Family"].unique().tolist())
# Paleta harmônica ampla, sem repetições próximas
palette_dark = [
    "#145efc", "#00796B", "#8E24AA", "#F57C00", "#388E3C", "#6D4C41",
    "#0288D1", "#7B1FA2", "#C62828", "#2E7D32", "#5D4037", "#283593",
    "#00897B", "#AD1457", "#512DA8", "#EF6C00", "#1976D2"
]
palette_light = [
    "#dbe7ff", "#b2dfdb", "#e1bee7", "#ffe0b2", "#c8e6c9", "#d7ccc8",
    "#b3e5fc", "#ce93d8", "#ffcdd2", "#a5d6a7", "#bcaaa4", "#c5cae9",
    "#80cbc4", "#f48fb1", "#d1c4e9", "#ffcc80", "#90caf9"
]

fam_colors_dark = {f: palette_dark[i % len(palette_dark)] for i, f in enumerate(families)}
fam_colors_light = {f: palette_light[i % len(palette_light)] for i, f in enumerate(families)}

# ===========================================================
# GRADE — FAMÍLIA, SUBFAMÍLIA, GRADES
# ===========================================================
grades = sorted(filtered["Global Grade"].unique(), key=lambda x: int(x) if x.isdigit() else x, reverse=True)
subfam_map = {
    f: sorted(filtered[filtered["Job Family"] == f]["Sub Job Family"].unique().tolist())
    for f in families
}

col_sizes = [120]
for f in families:
    col_sizes += [180 for _ in subfam_map[f]]
grid_template = f"grid-template-columns: {' '.join(str(x)+'px' for x in col_sizes)};"

# ===========================================================
# CONSTRUÇÃO HTML
# ===========================================================
html = "<div class='map-wrapper'>"

# LINHA 1 — Famílias (GG mesclado)
html += f"<div class='jobmap-grid sticky-header' style='{grid_template}; z-index:5;'>"
html += "<div class='grade-header'>GG</div>"
for f in families:
    span = len(subfam_map[f])
    color = fam_colors_dark[f]
    html += f"<div class='header-family' style='grid-column: span {span}; background:{color};'>{f}</div>"
html += "</div>"

# LINHA 2 — Subfamílias (sem linha intermediária)
html += f"<div class='jobmap-grid sticky-subheader' style='{grid_template}; z-index:4;'>"
html += "<div class='grade-cell'></div>"
for f in families:
    for sf in subfam_map[f]:
        color = fam_colors_light[f]
        html += f"<div class='header-subfamily' style='background:{color};'>{sf}</div>"
html += "</div>"

# LINHAS DE GG
for g in grades:
    html += f"<div class='jobmap-grid grade-row' style='{grid_template}; z-index:1;'>"
    html += f"<div class='grade-cell'>GG {g}</div>"
    for f in families:
        fam_df = filtered[filtered["Job Family"] == f]
        for sf in subfam_map[f]:
            cell_df = fam_df[(fam_df["Sub Job Family"] == sf) & (fam_df["Global Grade"] == g)]
            if not cell_df.empty:
                cards = "".join([
                    f"<div class='job-card'><b>{r['Job Profile']}</b><span>{r['Career Path']}</span></div>"
                    for _, r in cell_df.iterrows()
                ])
                html += f"<div>{cards}</div>"
            else:
                html += "<div></div>"
    html += "</div>"

html += "</div>"
st.markdown(html, unsafe_allow_html=True)
