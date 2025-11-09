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

# ===========================================================
# CABEÇALHO FIXO
# ===========================================================
st.markdown("""
<style>
.block-container {
  max-width: 1800px !important;
  padding-top: 0 !important;
}

/* ======= CABEÇALHO ======= */
.top-fixed {
  position: sticky;
  top: 0;
  z-index: 200;
  background-color: white;
  padding: 10px 0 14px 0;
  border-bottom: 2px solid #e0e0e0;
}
h1 {
  color: #145efc !important;
  font-weight: 800 !important;
  font-size: 1.8rem !important;
  margin-bottom: 0.6rem !important;
  display: flex; align-items: center; gap: 8px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='top-fixed'>", unsafe_allow_html=True)
section("🗺️ Job Map")

col1, col2 = st.columns([2, 2])
with col1:
    family_filter = st.selectbox("Família", ["Todas"])
with col2:
    path_filter = st.selectbox("Trilha de Carreira", ["Todas"])
st.markdown("</div>", unsafe_allow_html=True)

# ===========================================================
# CSS DO GRID
# ===========================================================
st.markdown("""
<style>
.map-wrapper {
  overflow-x: auto;
  overflow-y: auto;
  border-top: 3px solid #145efc;
  border-bottom: 3px solid #145efc;
  background: #fff;
  scroll-behavior: smooth;
}

/* ======= GRADE PRINCIPAL ======= */
.jobmap-grid {
  display: grid;
  grid-template-columns: 140px repeat(auto-fill, minmax(180px, 1fr));
  border-collapse: collapse;
  font-size: 0.85rem;
  width: max-content;
  text-align: center;
  gap: 0;
}

/* ======= COLUNA GG ======= */
.grade-header {
  background: #000;
  color: #fff;
  font-weight: 800;
  font-size: 1rem;
  height: 88px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-right: 2px solid #fff;
  position: sticky;
  left: 0;
  top: 92px;
  z-index: 70 !important;
}
.grade-cell {
  background: #000;
  color: #fff;
  font-weight: 700;
  padding: 10px;
  position: sticky;
  left: 0;
  z-index: 50 !important;
  border-right: 2px solid #fff;
}

/* ======= FAMÍLIAS ======= */
.header-family {
  font-weight: 800;
  color: #fff;
  padding: 12px 10px;
  font-size: 1rem;
  border-right: 1px solid #fff;
  border-bottom: 2px solid #fff;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: sticky;
  top: 92px;
  z-index: 60 !important;
}

/* ======= SUBFAMÍLIAS ======= */
.header-subfamily {
  font-weight: 600;
  padding: 10px;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  white-space: normal;
  line-height: 1.25;
  border-right: 1px solid #fff;
  border-bottom: 2px solid #fff;
  height: 40px;
  position: sticky;
  top: 140px;
  z-index: 55 !important;
}

/* ======= CÉLULAS ======= */
.job-cell {
  padding: 12px 10px;
  text-align: left;
  background: #fff;
  vertical-align: top;
  box-sizing: border-box;
}
.job-card {
  background: #f9f9f9;
  border-left: 4px solid #145efc;
  border-radius: 8px;
  padding: 10px 12px;
  margin: 8px 0;
  text-align: left;
  font-size: 0.82rem;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
  white-space: normal;
  word-wrap: break-word;
  overflow-wrap: break-word;
}
.job-card b {
  font-weight: 700;
  display: block;
  margin-bottom: 3px;
}
.job-card span {
  display: block;
  font-size: 0.75rem;
  color: #555;
}

/* ======= LINHAS ZEBRADAS ======= */
.grade-row:nth-child(even) {
  background: #fcfcfc;
}

/* ======= SCROLL E ZOOM ======= */
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

if family_filter != "Todas":
    df = df[df["Job Family"] == family_filter]
if path_filter != "Todas":
    df = df[df["Career Path"] == path_filter]

if df.empty:
    st.warning("Nenhum cargo encontrado com os filtros selecionados.")
    st.stop()

# ===========================================================
# CORES (familia + subfamilia)
# ===========================================================
families = sorted(df["Job Family"].unique().tolist())
palette_dark = [
    "#5b6a91", "#85677b", "#8b6a3e", "#607d8b", "#5b8060", "#6d7388",
    "#a76a87", "#8b805a", "#708090", "#776c82"
]
palette_light = [
    "#edf0f9", "#f2edf3", "#f7f3ea", "#edf2f4", "#f1f4f1", "#f0f3f9",
    "#f9edf1", "#f7f5ea", "#eff3f4", "#f3f0f7"
]

fam_colors_dark = {f: palette_dark[i % len(palette_dark)] for i, f in enumerate(families)}
fam_colors_light = {f: palette_light[i % len(palette_light)] for i, f in enumerate(families)}

grades = sorted(df["Global Grade"].unique(), key=lambda x: int(x) if x.isdigit() else x, reverse=True)
subfam_map = {
    f: sorted(df[df["Job Family"] == f]["Sub Job Family"].unique().tolist())
    for f in families
}

# ===========================================================
# HTML GRID
# ===========================================================
html = "<div class='map-wrapper'>"

# ===== LINHA 1 (Famílias)
html += "<div class='jobmap-grid'>"
html += "<div class='grade-header'>GG</div>"
for f in families:
    span = len(subfam_map[f])
    html += f"<div class='header-family' style='grid-column: span {span}; background:{fam_colors_dark[f]};'>{f}</div>"
html += "</div>"

# ===== LINHA 2 (Subfamílias)
html += "<div class='jobmap-grid'>"
html += "<div class='grade-cell'></div>"
for f in families:
    for sf in subfam_map[f]:
        html += f"<div class='header-subfamily' style='background:{fam_colors_light[f]};'>{sf}</div>"
html += "</div>"

# ===== DEMAIS LINHAS (Cargos)
for g in grades:
    html += "<div class='jobmap-grid grade-row'>"
    html += f"<div class='grade-cell'>GG {g}</div>"
    for f in families:
        fam_df = df[df["Job Family"] == f]
        for sf in subfam_map[f]:
            cell_df = fam_df[(fam_df["Sub Job Family"] == sf) & (fam_df["Global Grade"] == g)]
            if not cell_df.empty:
                cards = "".join([
                    f"<div class='job-card'><b>{r['Job Profile']}</b><span>{r['Career Path']}</span></div>"
                    for _, r in cell_df.iterrows()
                ])
                html += f"<div class='job-cell'>{cards}</div>"
            else:
                html += "<div class='job-cell'></div>"
    html += "</div>"

html += "</div>"
st.markdown(html, unsafe_allow_html=True)
