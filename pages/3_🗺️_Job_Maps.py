import streamlit as st
import pandas as pd
from utils.data_loader import load_excel_data
from utils.ui_components import section, lock_sidebar

# ===========================================================
# CONFIGURAÇÃO DA PÁGINA
# ===========================================================
st.set_page_config(layout="wide", page_title="🗺️ Job Map")
lock_sidebar()
st.write("⚙️ Versão ativa: v2025.11.09.5")

# ===========================================================
# CSS GLOBAL
# ===========================================================
st.markdown("""
<style>
.block-container {
  max-width: 1700px !important;
  margin: 0 auto !important;
  padding-top: 0 !important;
}

/* ===== CABEÇALHO FIXO ===== */
.top-fixed {
  position: sticky;
  top: 0;
  z-index: 100;
  background-color: white;
  padding: 15px 0 10px 0;
  border-bottom: 2px solid #e0e0e0;
}
h1 {
  color: #145efc !important;
  font-weight: 800 !important;
  font-size: 1.8rem !important;
  margin: 0 !important;
  display: flex; align-items: center; gap: 8px;
}

/* ===== MAPA ===== */
.map-wrapper {
  overflow-x: auto;
  overflow-y: auto;
  border-top: 3px solid #145efc;
  border-bottom: 3px solid #145efc;
  background: #fff;
  white-space: nowrap;
}

/* ===== GRID ===== */
.jobmap-grid {
  display: grid;
  border-collapse: collapse;
  grid-auto-rows: minmax(65px, auto);
  font-size: 0.85rem;
  text-align: center;
  width: max-content;
  position: relative;
}
.jobmap-grid > div {
  border: 1px solid #d9d9d9;
  box-sizing: border-box;
  height: auto !important;
  min-height: 65px;
}

/* ===== COLUNA GG ===== */
.grade-header {
  font-weight: 800;
  font-size: 1rem;
  background: #000;
  color: #fff;
  padding: 16px 10px;
  position: sticky;
  top: 0;
  left: 0;
  z-index: 70 !important;
  text-align: center;
  border-right: 2px solid #fff;
  border-bottom: 1px solid #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  grid-row: span 2;
}
.grade-cell {
  background: #000;
  color: #fff;
  font-weight: 700;
  padding: 10px;
  position: sticky;
  left: 0;
  z-index: 60 !important;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #fff;
}

/* ===== CABEÇALHOS ===== */
.header-family {
  font-weight: 800;
  color: #fff;
  padding: 10px 12px;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-right: 1px solid #fff;
}
.header-subfamily {
  font-weight: 600;
  padding: 8px 10px;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  white-space: normal;
  line-height: 1.25;
  border-right: 1px solid #fff;
}

/* ===== CABEÇALHOS FIXOS ===== */
.sticky-family {
  position: sticky;
  top: 95px;
  z-index: 65 !important;
}
.sticky-subfamily {
  position: sticky;
  top: 135px;
  z-index: 64 !important;
}

/* ===== CÉLULAS ===== */
.job-card {
  background: #f9f9f9;
  border-left: 4px solid #145efc;
  border-radius: 6px;
  padding: 6px 10px;
  margin: 5px;
  text-align: left;
  font-size: 0.8rem;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
  word-wrap: break-word;
  white-space: normal;
  overflow-wrap: break-word;
  width: calc(100% - 12px);
  height: auto;
  min-height: 60px;
}
.job-card b {
  display: block;
  font-weight: 700;
  margin-bottom: 3px;
}
.job-card span {
  display: block;
  font-size: 0.75rem;
  color: #555;
}
.job-card:hover {
  background: #eef4ff;
}

/* ===== ZEBRA ===== */
.grade-row:nth-child(even) {
  background: #fcfcfc;
}

/* ===== GRID PRETO COM LINHAS BRANCAS ===== */
.grade-cell, .grade-header {
  border-top: 1px solid #fff;
  border-bottom: 1px solid #fff;
}

/* ===== AJUSTE VISUAL ===== */
.jobmap-grid > div:first-child {
  border-left: none;
}
</style>
""", unsafe_allow_html=True)

# ===========================================================
# FILTROS
# ===========================================================
st.markdown("<div class='top-fixed'>", unsafe_allow_html=True)
section("🗺️ Job Map")

data = load_excel_data()
df = data.get("job_profile", pd.DataFrame())

required_cols = ["Job Family", "Sub Job Family", "Job Profile", "Career Path", "Global Grade", "Full Job Code"]
missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error(f"Colunas ausentes no Excel: {', '.join(missing)}")
    st.stop()

df = df.dropna(subset=["Job Family", "Sub Job Family", "Job Profile", "Global Grade"])
df["Global Grade"] = df["Global Grade"].astype(str).str.replace(r"\\.0$", "", regex=True)

families = sorted(df["Job Family"].dropna().unique().tolist())
paths = sorted(df["Career Path"].dropna().unique().tolist())

col1, col2 = st.columns([2, 2])
with col1:
    family_filter = st.selectbox("Família", ["Todas"] + families)
with col2:
    path_filter = st.selectbox("Trilha de Carreira", ["Todas"] + paths)
st.markdown("</div>", unsafe_allow_html=True)

if family_filter != "Todas":
    df = df[df["Job Family"] == family_filter]
if path_filter != "Todas":
    df = df[df["Career Path"] == path_filter]

if df.empty:
    st.warning("Nenhum cargo encontrado com os filtros selecionados.")
    st.stop()

# ===========================================================
# PALETA ELEGANTE
# ===========================================================
families = sorted(df["Job Family"].unique().tolist())
palette_dark = ["#3B5BA9", "#4E7063", "#8B7B5A", "#2C4875", "#5C5C5C", "#6B4F6B"]
palette_light = ["#E6EBF8", "#E8F1ED", "#F0EDE6", "#E8EEF9", "#F4F4F4", "#EDE8F1"]

fam_colors_dark = {f: palette_dark[i % len(palette_dark)] for i, f in enumerate(families)}
fam_colors_light = {f: palette_light[i % len(palette_light)] for i, f in enumerate(families)}

grades = sorted(df["Global Grade"].unique(), key=lambda x: int(x) if x.isdigit() else x, reverse=True)
subfam_map = {
    f: sorted(df[df["Job Family"] == f]["Sub Job Family"].unique().tolist())
    for f in families
}

# Grid fluido ajustável
grid_template = f"grid-template-columns: 150px repeat({sum(len(subfam_map[f]) for f in families)}, minmax(220px, 1fr));"

# ===========================================================
# GRID VISUAL
# ===========================================================
html = "<div class='map-wrapper'>"

# LINHA 1 — Famílias (GG mesclado)
html += f"<div class='jobmap-grid sticky-family' style='{grid_template};'>"
html += "<div class='grade-header'>GG</div>"
for f in families:
    span = len(subfam_map[f])
    color = fam_colors_dark[f]
    html += f"<div class='header-family' style='grid-column: span {span}; background:{color};'>{f}</div>"
html += "</div>"

# LINHA 2 — Subfamílias
html += f"<div class='jobmap-grid sticky-subfamily' style='{grid_template};'>"
html += "<div class='grade-cell'></div>"
for f in families:
    for sf in subfam_map[f]:
        color = fam_colors_light[f]
        html += f"<div class='header-subfamily' style='background:{color};'>{sf}</div>"
html += "</div>"

# DEMAIS LINHAS — Grades e cargos
for g in grades:
    html += f"<div class='jobmap-grid grade-row' style='{grid_template};'>"
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
                html += f"<div style='padding:6px 8px;'>{cards}</div>"
            else:
                html += "<div></div>"
    html += "</div>"

html += "</div>"
st.markdown(html, unsafe_allow_html=True)
