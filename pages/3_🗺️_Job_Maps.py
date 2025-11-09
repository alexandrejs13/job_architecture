import streamlit as st
import pandas as pd
import random
from utils.data_loader import load_job_profile_df

# ===========================================================
# CONFIGURAÇÃO DA PÁGINA
# ===========================================================
st.set_page_config(layout="wide", page_title="🗺️ Job Map")

# ===========================================================
# CSS — Visual clean refinado
# ===========================================================
st.markdown("""
<style>
.block-container {
  max-width: 1700px !important;
  margin: 0 auto !important;
}

/* ======= TÍTULO ======= */
h1 {
  color: #1E56E0 !important;
  font-weight: 800 !important;
  font-size: 1.9rem !important;
  margin-bottom: 1rem !important;
}

/* ======= ÁREA DE SCROLL ======= */
.map-wrapper {
  overflow: auto;
  border-top: 3px solid #A3B8F0;
  border-bottom: 3px solid #A3B8F0;
  background: #fff;
  padding-bottom: 1rem;
  white-space: nowrap;
}

/* ======= GRID PRINCIPAL ======= */
.jobmap-grid {
  display: grid;
  border-collapse: collapse;
  font-size: 0.88rem;
  text-align: center;
  width: max-content;
  position: relative;
}
.jobmap-grid > div {
  border: 1px solid #ddd;
  box-sizing: border-box;
}

/* ======= CABEÇALHOS ======= */
.header-family {
  font-weight: 800;
  color: #fff;
  padding: 8px;
  background: #4A74E8;
  white-space: normal;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 40px;
}
.header-subfamily {
  font-weight: 600;
  background: #E9ECF9;
  padding: 6px;
  white-space: normal;
  font-size: 0.95rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #1E56E0;
  height: 38px;
}

/* ======= FIXAR CABEÇALHOS ======= */
.header-family, .header-subfamily {
  position: sticky;
  z-index: 35;
}
.header-family { top: 0; }
.header-subfamily { top: 40px; }

/* ======= COLUNA “GG” FIXA ======= */
.grade-header {
  font-weight: 800;
  font-size: 0.95rem;
  background: #1E56E0;
  color: #fff;
  padding: 8px;
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
  background: #F3F6FD;
  border-right: 2px solid #A3B8F0;
  padding: 6px 8px;
  position: sticky;
  left: 0;
  z-index: 30 !important;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ======= CÉLULAS DE CARGO ======= */
.job-card {
  background: #fafafa;
  border-left: 4px solid #A3B8F0;
  border-radius: 6px;
  padding: 6px 8px;
  margin: 3px 0;
  text-align: left;
  font-size: 0.85rem;
  box-shadow: 0 1px 2px rgba(0,0,0,0.04);
  white-space: normal;
}
.job-card b {
  font-weight: 700;
}
.job-card span {
  display: block;
  font-size: 0.78rem;
  color: #444;
  font-weight: 400;
}
.job-card:hover {
  background: #f5f7ff;
}

/* ======= ZEBRA ======= */
.grade-row:nth-child(even) { background: #fcfcfc; }

/* ======= RESPONSIVIDADE ======= */
@media (max-width: 1500px) { .block-container { zoom: 0.9; } }
@media (max-width: 1200px) { .block-container { zoom: 0.85; } }
</style>
""", unsafe_allow_html=True)

# ===========================================================
# LEITURA DE DADOS
# ===========================================================
try:
    df = load_job_profile_df()
except Exception as e:
    st.error(f"❌ Erro ao carregar Job Profile.xlsx: {e}")
    st.stop()

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
# CORES POR FAMÍLIA (SUAVES)
# ===========================================================
families = sorted(filtered["Job Family"].unique().tolist())
random.seed(10)
palette = [
    "#A3B8F0", "#BFD8B8", "#F4C7AB", "#F7D9C4", "#C5DFF8", "#D0E8C5",
    "#F8EDE3", "#FAD9C1", "#D6E2E9", "#CDEAC0", "#F9EBC8"
]
fam_colors = {f: palette[i % len(palette)] for i, f in enumerate(families)}

# ===========================================================
# GRADE HORIZONTAL
# ===========================================================
grades = sorted(
    filtered["Global Grade"].unique(),
    key=lambda x: int(x) if x.isdigit() else x,
    reverse=True
)

subfam_map = {
    f: sorted(filtered[filtered["Job Family"] == f]["Sub Job Family"].unique().tolist())
    for f in families
}

col_sizes = [110]
for f in families:
    for sf in subfam_map[f]:
        width = max(140, len(sf) * 8)  # ajusta largura ao texto
        col_sizes.append(width)

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
html += "<div class='grade-cell'></div>"
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
                    f"<div class='job-card'><b>{r['Job Profile']}</b><span>{r['Career Path']}</span></div>"
                    for _, r in cell_df.iterrows()
                ])
                html += f"<div>{cards}</div>"
            else:
                html += "<div></div>"
    html += "</div>"

html += "</div>"
st.markdown(html, unsafe_allow_html=True)
