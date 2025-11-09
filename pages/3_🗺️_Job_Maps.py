# pages/3_🗺️_Job_Maps.py
# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
from utils.data_loader import load_excel_data
from utils.ui_components import section, lock_sidebar

# ===========================================================
# CONFIGURAÇÃO DE PÁGINA
# ===========================================================
st.set_page_config(layout="wide", page_title="🗺️ Job Map")
lock_sidebar()

# ===========================================================
# CSS PRINCIPAL
# ===========================================================
st.markdown("""
<style>
:root {
  --blue: #145efc;
  --gray-line: #e4e6eb;
  --gray-bg: #fafafa;
}

/* ===== CONTAINER PRINCIPAL ===== */
.block-container {
  max-width: 1720px !important;
  min-width: 1420px !important;
  margin: 0 auto !important;
  padding-top: 0 !important;
}

/* ===== TOPO FIXO ===== */
.top-fixed {
  position: sticky;
  top: 0;
  z-index: 100;
  background-color: white;
  padding: 14px 0 12px 0;
  border-bottom: 2px solid var(--gray-line);
}
h1 {
  color: var(--blue) !important;
  font-weight: 900 !important;
  font-size: 1.9rem !important;
  display: flex; align-items:center; gap:8px;
  margin: 0 0 8px 0 !important;
}

/* ===== GRID GERAL ===== */
.map-wrapper {
  overflow: auto;
  border-top: 3px solid var(--blue);
  border-bottom: 3px solid var(--blue);
  background: white;
  white-space: nowrap;
}
.jobmap-grid {
  display: grid;
  grid-auto-rows: auto;
  border-collapse: collapse;
  width: max-content;
  font-size: 0.9rem;
  border-right: 1px solid var(--gray-line);
  border-bottom: 1px solid var(--gray-line);
}
.jobmap-grid > div {
  border-right: 1px solid var(--gray-line);
  border-bottom: 1px solid var(--gray-line);
  box-sizing: border-box;
}

/* ===== COLUNA GG ===== */
.gg-header {
  background: black;
  color: white;
  font-weight: 800;
  text-align: center;
  position: sticky;
  left: 0;
  z-index: 60 !important;
  border-right: 1px solid white;
  display:flex; align-items:center; justify-content:center;
  grid-row: span 2;
}
.gg-row {
  background: black;
  color: white;
  font-weight: 700;
  text-align: center;
  position: sticky;
  left: 0;
  z-index: 50 !important;
  border-right: 1px solid white;
  border-top: 1px solid white;
  display:flex; align-items:center; justify-content:center;
}

/* ===== CABEÇALHOS ===== */
.header-family {
  font-weight: 800;
  color: white;
  text-align: center;
  padding: 10px 6px;
  display:flex; align-items:center; justify-content:center;
  border-bottom: 1px solid white;
  white-space: normal; line-height: 1.25;
  position: sticky;
  top: 0;
  z-index: 55;
}
.header-subfamily {
  font-weight: 700;
  background: #f3f4f7;
  color: #333;
  text-align: center;
  padding: 8px 6px;
  display:flex; align-items:center; justify-content:center;
  white-space: normal; line-height: 1.2;
  border-top: 1px solid white;
  position: sticky;
  top: 48px;
  z-index: 54;
}

/* ===== CÉLULAS ===== */
.cell {
  padding: 6px;
  background: white;
  min-height: 58px;
}
.job-card {
  background: var(--gray-bg);
  border-left: 4px solid var(--blue);
  border-radius: 8px;
  padding: 8px 10px;
  margin: 4px 3px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.06);
  font-size: 0.9rem;
  text-align: left;
  word-wrap: break-word;
  overflow-wrap: break-word;
  white-space: normal;
  line-height: 1.25;
}
.job-card b {
  display:block;
  font-weight:800;
  margin-bottom: 3px;
  word-break: break-word;
  white-space: normal;
}
.job-card span {
  display:block;
  font-size:0.82rem;
  color:#555;
}

/* ===== FAMÍLIA E SUBFAMÍLIA ===== */
.family-divider {
  box-shadow: inset -2px 0 0 0 white;
}

/* ===== RESPONSIVIDADE ===== */
@media (max-width: 1500px) { .block-container { zoom: 0.9; } }
@media (max-width: 1200px) { .block-container { zoom: 0.8; } }
</style>
""", unsafe_allow_html=True)

# ===========================================================
# DADOS E FILTROS
# ===========================================================
data = load_excel_data()
df = data.get("job_profile", pd.DataFrame())

required = ["Job Family","Sub Job Family","Job Profile","Career Path","Global Grade","Full Job Code"]
missing = [c for c in required if c not in df.columns]
if missing:
    st.error(f"Colunas ausentes no Excel: {', '.join(missing)}")
    st.stop()

df = df.dropna(subset=["Job Family","Sub Job Family","Job Profile","Global Grade"])
df["Global Grade"] = df["Global Grade"].astype(str).str.replace(r"\.0$","",regex=True)

st.markdown("<div class='top-fixed'>", unsafe_allow_html=True)
section("🗺️ Job Map")

col1, col2 = st.columns([2,2])
families = ["Todas"] + sorted(df["Job Family"].unique().tolist())
paths = ["Todas"] + sorted(df["Career Path"].unique().tolist())
with col1:
    family_filter = st.selectbox("Família", families)
with col2:
    path_filter = st.selectbox("Trilha de Carreira", paths)
st.markdown("</div>", unsafe_allow_html=True)

if family_filter != "Todas":
    df = df[df["Job Family"] == family_filter]
if path_filter != "Todas":
    df = df[df["Career Path"] == path_filter]
if df.empty:
    st.warning("Nenhum cargo encontrado com os filtros selecionados.")
    st.stop()

# ===========================================================
# ORGANIZAÇÃO E CORES
# ===========================================================
familias = sorted(df["Job Family"].unique().tolist())
palette_dark = ["#4B5A73","#606B78","#6E7065","#7B6C7F","#857160","#5B6C80","#6F6578","#7A715D"]
palette_light = ["#E8EBF2","#ECEEF0","#EFF1EA","#F2EFF3","#F4F0EB","#EAF0F5","#F0EEF4","#F3F2ED"]
cores_familia = {f:palette_dark[i%len(palette_dark)] for i,f in enumerate(familias)}
cores_subfam  = {f:palette_light[i%len(palette_light)] for i,f in enumerate(familias)}
grades = sorted(df["Global Grade"].unique(), key=lambda x:int(x) if x.isdigit() else 999, reverse=True)
subfamilias = {f:sorted(df[df["Job Family"]==f]["Sub Job Family"].unique().tolist()) for f in familias}

# ===========================================================
# CALCULAR LARGURA DAS COLUNAS (DINÂMICA)
# ===========================================================
def largura(text):
    base=len(str(text)); return min(max(200,base*9+40),420)
col_larguras=["160px"]
for f in familias:
    for s in subfamilias[f]:
        maior = max([s]+df[(df["Job Family"]==f)&(df["Sub Job Family"]==s)]["Job Profile"].tolist(),key=len)
        col_larguras.append(f"{largura(maior)}px")
grid_cols = f"grid-template-columns: {' '.join(col_larguras)};"

# ===========================================================
# RENDERIZAÇÃO HTML (UM ÚNICO GRID)
# ===========================================================
html=[]
html.append("<div class='map-wrapper'>")
html.append(f"<div class='jobmap-grid' style='{grid_cols}'>")

# GG (mesclado)
html.append("<div class='gg-header'><div>GG</div></div>")
for f in familias:
    span=len(subfamilias[f])
    html.append(f"<div class='header-family family-divider' style='grid-column: span {span}; background:{cores_familia[f]};'>{f}</div>")
for f in familias:
    for s in subfamilias[f]:
        html.append(f"<div class='header-subfamily family-divider' style='background:{cores_subfam[f]};'>{s}</div>")

for g in grades:
    html.append(f"<div class='gg-row'><div>GG {g}</div></div>")
    for f in familias:
        fam_df=df[df["Job Family"]==f]
        for s in subfamilias[f]:
            c=fam_df[(fam_df["Sub Job Family"]==s)&(fam_df["Global Grade"]==g)]
            if c.empty:
                html.append("<div class='cell'></div>")
            else:
                cards="".join([f"<div class='job-card'><b>{r['Job Profile']}</b><span>{r['Career Path']}</span></div>" for _,r in c.iterrows()])
                html.append(f"<div class='cell'>{cards}</div>")

html.append("</div></div>")
st.markdown("".join(html), unsafe_allow_html=True)
