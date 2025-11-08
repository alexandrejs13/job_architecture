import streamlit as st
import pandas as pd
import io, base64, random

# ===========================================================
# CONFIG
# ===========================================================
st.set_page_config(layout="wide", page_title="🗺️ Job Map")

st.markdown("""
<style>
.block-container {
  max-width: 1700px !important;
  min-width: 1700px !important;
  margin: 0 auto !important;
}

/* ======= HEADER ======= */
h1 {
  color: #1E56E0 !important;
  font-weight: 800 !important;
  font-size: 1.8rem !important;
  margin-bottom: 1rem !important;
  display: flex; align-items: center; gap: 8px;
}

/* ======= ÁREA DE SCROLL ======= */
.map-wrapper {
  overflow-x: auto;
  overflow-y: hidden;
  border-top: 3px solid #1E56E0;
  border-bottom: 3px solid #1E56E0;
  background: #fff;
  padding-bottom: 1rem;
  white-space: nowrap;
}

/* ======= GRID ======= */
.jobmap-grid {
  display: grid;
  border-collapse: collapse;
  font-size: 0.85rem;
  text-align: center;
  width: max-content;
  z-index: 0;
}
.jobmap-grid > div {
  border: 1px solid #ddd;
  box-sizing: border-box;
}

/* ======= CABEÇALHOS ======= */
.header-family {
  font-weight: 800;
  color: #fff;
  padding: 10px;
  border-right: 2px solid #fff;
  white-space: normal;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}
.header-subfamily {
  font-weight: 700;
  background: #f0f2ff;
  padding: 8px;
  white-space: normal;
  font-size: 0.95rem;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

/* ======= COLUNA “GG” FIXA ======= */
.grade-header {
  font-weight: 800;
  font-size: 0.95rem;
  background: #1E56E0;
  color: #fff;
  padding: 8px;
  border-right: 2px solid #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  position: sticky;
  top: 0;
  left: 0;
  z-index: 40 !important;
}
.grade-cell {
  font-weight: 700;
  background: #eef3ff;
  border-right: 2px solid #1E56E0;
  padding: 6px 8px;
  position: sticky;
  left: 0;
  z-index: 30 !important;
  display: flex;
  align-items: center;
  justify-content: center;
}
.grade-cell::after {
  content: "";
  position: absolute;
  right: 0;
  top: 0;
  height: 100%;
  width: 2px;
  background: rgba(0,0,0,0.05);
}

/* ======= CARDS ======= */
.job-card {
  background: #fafafa;
  border-left: 4px solid #1E56E0;
  border-radius: 6px;
  padding: 5px 8px;
  margin: 3px 0;
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
  background: #f0f5ff;
}

/* ======= ZEBRA ======= */
.grade-row:nth-child(even) {
  background: #fcfcfc;
}

/* ======= RESPONSIVIDADE ======= */
@media (max-width: 1500px) { .block-container { zoom: 0.9; } }
@media (max-width: 1200px) { .block-container { zoom: 0.8; } }
</style>
""", unsafe_allow_html=True)

# ===========================================================
# DADOS
# ===========================================================
from utils.data_loader import load_data
data = load_data()

if "job_profile" not in data:
    st.error("⚠️ Arquivo 'Job Profile.csv' não encontrado.")
    st.stop()

df = data["job_profile"]

required_cols = ["Job Family", "Sub Job Family", "Job Profile", "Career Path", "Global Grade", "Full Job Code"]
missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error(f"Colunas ausentes no CSV: {', '.join(missing)}")
    st.stop()

df = df.dropna(subset=["Job Family", "Sub Job Family", "Job Profile", "Global Grade"])
df["Global Grade"] = df["Global Grade"].astype(str).str.replace(r"\\.0$", "", regex=True)

# ===========================================================
# FILTROS
# ===========================================================
st.markdown("<h1>🗺️ Job Map</h1>", unsafe_allow_html=True)
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
# CORES POR FAMÍLIA
# ===========================================================
families = sorted(filtered["Job Family"].unique().tolist())
random.seed(10)
palette = [
    "#1E56E0", "#00796B", "#9C27B0", "#E65100", "#5D4037", "#0288D1",
    "#558B2F", "#8E24AA", "#F9A825", "#6D4C41", "#0097A7"
]
fam_colors = {f: palette[i % len(palette)] for i, f in enumerate(families)}

# ===========================================================
# GRADE HORIZONTAL
# ===========================================================
# Ordena do MAIOR para o MENOR
grades = sorted(filtered["Global Grade"].unique(),
                key=lambda x: int(x) if x.isdigit() else x,
                reverse=True)

subfam_map = {f: sorted(filtered[filtered["Job Family"] == f]["Sub Job Family"].unique().tolist()) for f in families}

col_sizes = [100]
for f in families:
    col_sizes += [140 for _ in subfam_map[f]]
grid_template = f"grid-template-columns: {' '.join(str(x)+'px' for x in col_sizes)};"

html = "<div class='map-wrapper'>"

# Cabeçalho 1 (Família)
html += f"<div class='jobmap-grid' style='{grid_template}; z-index:5;'>"
html += "<div class='grade-header'>GG</div>"
for f in families:
    span = len(subfam_map[f])
    color = fam_colors[f]
    html += f"<div class='header-family' style='grid-column: span {span}; background:{color};'>{f}</div>"
html += "</div>"

# Cabeçalho 2 (Subfamily)
html += f"<div class='jobmap-grid' style='{grid_template}; z-index:4;'>"
html += "<div class='grade-cell' style='background:#eef3ff; z-index:32 !important;'></div>"
for f in families:
    for sf in subfam_map[f]:
        html += f"<div class='header-subfamily'>{sf}</div>"
html += "</div>"

# Linhas (Grades)
for g in grades:
    html += f"<div class='jobmap-grid grade-row' style='{grid_template}; z-index:1;'>"
    html += f"<div class='grade-cell'>GG {g}</div>"
    for f in families:
        fam_df = filtered[filtered["Job Family"] == f]
        for sf in subfam_map[f]:
            cell_df = fam_df[(fam_df["Sub Job Family"] == sf) & (fam_df["Global Grade"] == g)]
            if not cell_df.empty:
                cards = "".join([
                    f"<div class='job-card' title='{r['Full Job Code']}'><b>{r['Job Profile']}</b><span>{r['Career Path']}</span></div>"
                    for _, r in cell_df.iterrows()
                ])
                html += f"<div>{cards}</div>"
            else:
                html += "<div></div>"
    html += "</div>"

html += "</div>"
st.markdown(html, unsafe_allow_html=True)
