import streamlit as st
import pandas as pd
import random
from utils.data_loader import load_excel_data
from utils.ui_components import section, lock_sidebar

# ===========================================================
# CONFIGURAÇÃO DA PÁGINA (deve vir primeiro!)
# ===========================================================
st.set_page_config(layout="wide", page_title="🗺️ Job Map")
lock_sidebar()

# ===========================================================
# IDENTIFICAÇÃO DE VERSÃO ATIVA
# ===========================================================
st.write("⚙️ Versão ativa: v2025.11.09.2")

# ===========================================================
# CSS GLOBAL — VISUAL LIMPO E TÉCNICO
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
  font-size: 0.85rem;
  text-align: center;
  width: max-content;
  position: relative;
}
.jobmap-grid > div {
  border: 1px solid #fff;
  box-sizing: border-box;
}

/* ===== COLUNA GG ===== */
.grade-header {
  font-weight: 800;
  font-size: 1rem;
  background: #000;
  color: #fff;
  padding: 12px 10px;
  position: sticky;
  top: 0;
  left: 0;
  z-index: 70 !important;
  text-align: center;
  vertical-align: middle;
  border-right: 2px solid #fff;
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
  border-bottom: 1px solid #fff; /* grid branco entre GGs */
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
  line-height: 1.2;
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
  border-radius: 8px;
  padding: 6px 8px;
  margin: 4px 5px;
  text-align: left;
  font-size: 0.8rem;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
  word-wrap: break-word;
  overflow-wrap: break-word;
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

/* ===== ZEBRA / GRID ===== */
.grade-row:nth-child(even) {
  background: #fcfcfc;
}

/* ===== ESPAÇAMENTO / RESPONSIVIDADE ===== */
@media (max-width: 1500px) { .block-container { zoom: 0.9; } }
@media (max-width: 1200px) { .block-container { zoom: 0.8; } }
</style>
""", unsafe_allow_html=True)

# ===========================================================
# TÍTULO E FILTROS FIXOS
# ===========================================================
st.markdown("<div class='top-fixed'>", unsafe_allow_html=True)
section("🗺️ Job Map")

col1, col2 = st.columns([2, 2])
with col1:
    family_filter = st.selectbox("Família", ["Todas"])
with col2:
    path_filter = st.selectbox("Trilha de Carreira", ["Todas"])
st.markdown("</div>", unsafe_allow_html=True)

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
# CORES SUAVES E HARMÔNICAS
# ===========================================================
families = sorted(df["Job Family"].unique().tolist())
palette_dark = [
    "#145efc", "#00796B", "#9C27B0", "#E65100", "#5D4037", "#0288D1",
    "#558B2F", "#8E24AA", "#F9A825", "#6D4C41"
]
palette_light = [
    "#e6ecff", "#e8f5e9", "#f3e5f5", "#fbe9e7", "#efebe9", "#e1f5fe",
    "#f1f8e9", "#f3e5f5", "#fffde7", "#efebe9"
]

fam_colors_dark = {f: palette_dark[i % len(palette_dark)] for i, f in enumerate(families)}
fam_colors_light = {f: palette_light[i % len(palette_light)] for i, f in enumerate(families)}

grades = sorted(df["Global Grade"].unique(), key=lambda x: int(x) if x.isdigit() else x, reverse=True)
subfam_map = {
    f: sorted(df[df["Job Family"] == f]["Sub Job Family"].unique().tolist())
    for f in families
}

col_sizes = [150]
for f in families:
    col_sizes += [220 for _ in subfam_map[f]]
grid_template = f"grid-template-columns: {' '.join(str(x)+'px' for x in col_sizes)};"

# ===========================================================
# CONSTRUÇÃO VISUAL DO GRID
# ===========================================================
html = "<div class='map-wrapper'>"

# LINHA 1 — Famílias (GG mesclado)
html += f"<div class='jobmap-grid sticky-family' style='{grid_template};'>"
html += "<div class='grade-header' style='grid-row: span 2;'>GG</div>"
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
