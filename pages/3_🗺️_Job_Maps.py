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
# CSS E ESTILO GERAL
# ===========================================================
st.markdown("""
<style>
.block-container {
  max-width: 1700px !important;
  min-width: 1500px !important;
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
</style>
""", unsafe_allow_html=True)

# ===========================================================
# CABEÇALHO E FILTROS
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
# CSS PRINCIPAL DO GRID
# ===========================================================
st.markdown("""
<style>
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
  border: 1px solid #ddd;
  box-sizing: border-box;
}

/* ===== GG (PRIMEIRA COLUNA) ===== */
.grade-header {
  font-weight: 800;
  font-size: 1rem;
  background: #000;
  color: #fff;
  padding: 12px;
  position: sticky;
  top: 0;
  left: 0;
  z-index: 100 !important;
  text-align: center;
  border-right: 2px solid #fff;
}
.grade-cell {
  font-weight: 700;
  background: #000;
  color: #fff;
  padding: 10px;
  position: sticky;
  left: 0;
  z-index: 90 !important;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #fff;
}

/* ===== FAMÍLIA ===== */
.header-family {
  font-weight: 800;
  color: #fff;
  padding: 12px 10px;
  font-size: 1rem;
  border-right: 1px solid #fff;
  text-align: center;
  display: flex; align-items: center; justify-content: center;
  line-height: 1.25;
}

/* ===== SUBFAMÍLIA ===== */
.header-subfamily {
  font-weight: 600;
  background: #f3f4f9;
  padding: 10px;
  font-size: 0.9rem;
  display: flex; align-items: center; justify-content: center;
  white-space: normal; line-height: 1.25;
  border-right: 1px solid #fff;
  border-top: none !important;
}

/* ===== FIXAR FAMÍLIA E SUBFAMÍLIA ===== */
.sticky-family { position: sticky; top: 0; z-index: 85 !important; }
.sticky-subfamily { position: sticky; top: 40px; z-index: 84 !important; }

/* ===== CARDS ===== */
.job-card {
  background: #f9f9f9;
  border-left: 4px solid #145efc;
  border-radius: 8px;
  padding: 8px 10px;
  margin: 5px 4px;
  text-align: left;
  font-size: 0.82rem;
  box-shadow: 0 1px 2px rgba(0,0,0,0.06);
  word-wrap: break-word;
  overflow-wrap: break-word;
}
.job-card b {
  display: block;
  font-weight: 700;
  margin-bottom: 2px;
}
.job-card span {
  display: block;
  font-size: 0.75rem;
  color: #555;
}
.job-card:hover { background: #eef4ff; }

/* ===== CORES SUAVES ===== */
.grade-row:nth-child(even) { background: #fcfcfc; }

/* ===== RESPONSIVIDADE ===== */
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
# PALETA DE CORES SUAVES E ELEGANTES
# ===========================================================
families = [
    "Top Executive/General Management", "Corporate Affairs/Communications",
    "Legal & Internal Audit", "Finance", "IT", "People & Culture",
    "Sales", "Marketing", "Technical Services", "Research & Development",
    "Technical Engineering", "Operations", "Supply Chain & Logistics",
    "Quality Management", "Facility & Administrative Services"
]
palette_dark = [
    "#2C3E50", "#4B3869", "#006D77", "#2F4858", "#4C5B5C", "#5C5470",
    "#3D405B", "#264653", "#1E3D59", "#344E41", "#2A4D69", "#264653",
    "#3B3C36", "#243B55", "#2B3A67"
]
palette_light = [
    "#E0E7EF", "#EAE4F2", "#E1F0F1", "#E6EBEE", "#EAECEC", "#EAE8F2",
    "#E5E6EC", "#E3E8EB", "#E2E6EA", "#E4EBE8", "#E3E8EF", "#E3E8EC",
    "#E7E7E3", "#E6EBF2", "#E3E6F0"
]

fam_colors_dark = {f: palette_dark[i % len(palette_dark)] for i, f in enumerate(families)}
fam_colors_light = {f: palette_light[i % len(palette_light)] for i, f in enumerate(families)}

grades = sorted(df["Global Grade"].unique(), key=lambda x: int(x) if x.isdigit() else x, reverse=True)
subfam_map = {f: sorted(df[df["Job Family"] == f]["Sub Job Family"].unique().tolist()) for f in families if f in df["Job Family"].unique()}

col_sizes = [150]
for f in families:
    if f in subfam_map:
        col_sizes += [220 for _ in subfam_map[f]]
grid_template = f"grid-template-columns: {' '.join(str(x)+'px' for x in col_sizes)};"

# ===========================================================
# CONSTRUÇÃO VISUAL
# ===========================================================
html = "<div class='map-wrapper'>"

# LINHA 1 — GG + FAMÍLIA
html += f"<div class='jobmap-grid sticky-family' style='{grid_template};'>"
html += "<div class='grade-header' rowspan='2'>GG</div>"
for f in families:
    if f in subfam_map:
        span = len(subfam_map[f])
        color = fam_colors_dark[f]
        html += f"<div class='header-family' style='grid-column: span {span}; background:{color};'>{f}</div>"
html += "</div>"

# LINHA 2 — SUBFAMÍLIAS (SEM LINHA FANTASMA)
html += f"<div class='jobmap-grid sticky-subfamily' style='{grid_template};'>"
html += "<div class='grade-cell'></div>"
for f in families:
    if f in subfam_map:
        for sf in subfam_map[f]:
            color = fam_colors_light[f]
            html += f"<div class='header-subfamily' style='background:{color};'>{sf}</div>"
html += "</div>"

# DEMAIS LINHAS — CARGOS
for g in grades:
    html += f"<div class='jobmap-grid grade-row' style='{grid_template};'>"
    html += f"<div class='grade-cell'>GG {g}</div>"
    for f in families:
        if f in subfam_map:
            fam_df = df[df["Job Family"] == f]
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
