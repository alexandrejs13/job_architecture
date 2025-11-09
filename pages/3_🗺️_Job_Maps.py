# -*- coding: utf-8 -*-
# pages/3_🗺️_Job_Maps.py

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
# CSS COMPLETO
# ===========================================================
st.markdown("""
<style>
:root {
  --blue: #145efc;
  --sand1: #f2efeb;
  --sand2: #e5dfd9;
  --sand3: #bfbab5;
  --sand4: #73706d;
  --moss1: #f5f073;
  --moss2: #c8c846;
  --moss3: #a0a905;
  --forest1: #4fa593;
  --forest2: #167665;
  --forest3: #00493b;
  --spark: #dca0ff;
  --sky: #145efc;
  --gray: #f6f6f7;
  --line: #ddd;
}

/* ======= BLOCO PRINCIPAL ======= */
.block-container {
  max-width: 1700px !important;
  margin: 0 auto !important;
  padding: 0 !important;
}

/* ======= CABEÇALHO FIXO ======= */
.topbar {
  position: sticky;
  top: 0;
  z-index: 100;
  background: white;
  padding: 15px 0 8px 0;
  border-bottom: 2px solid var(--blue);
}
h1 {
  color: var(--blue);
  font-weight: 900 !important;
  font-size: 1.9rem !important;
  display: flex; align-items: center; gap: 8px;
  margin-bottom: 12px !important;
}

/* ======= ÁREA DE MAPA ======= */
.map-wrapper {
  overflow: auto;
  background: white;
  border-top: 3px solid var(--blue);
  border-bottom: 3px solid var(--blue);
  white-space: nowrap;
}

/* ======= GRID PRINCIPAL ======= */
.jobmap-grid {
  display: grid;
  border-collapse: collapse;
  width: max-content;
  font-size: 0.88rem;
  text-align: center;
  border-right: 1px solid var(--line);
  border-bottom: 1px solid var(--line);
}
.jobmap-grid > div {
  border: 1px solid var(--line);
  box-sizing: border-box;
}

/* ======= COLUNA GG ======= */
.gg-header {
  background: black;
  color: white;
  font-weight: 800;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  grid-row: span 2;
  position: sticky;
  left: 0;
  z-index: 60;
  border-right: 2px solid white;
}
.gg-cell {
  background: black;
  color: white;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  position: sticky;
  left: 0;
  z-index: 55;
  border-right: 2px solid white;
  border-top: 1px solid white;
}

/* ======= CABEÇALHOS ======= */
.header-family {
  font-weight: 800;
  color: white;
  text-align: center;
  padding: 12px 6px;
  border-bottom: 1px solid white;
  position: sticky;
  top: 0;
  z-index: 52;
  display: flex;
  align-items: center;
  justify-content: center;
  white-space: normal;
}
.header-subfamily {
  font-weight: 700;
  text-align: center;
  padding: 10px 6px;
  border-bottom: 1px solid white;
  position: sticky;
  top: 48px;
  z-index: 51;
  display: flex;
  align-items: center;
  justify-content: center;
  white-space: normal;
  background: var(--gray);
}

/* ======= CÉLULAS ======= */
.cell {
  padding: 8px;
  background: white;
  text-align: left;
  min-height: 64px;
  vertical-align: middle;
}
.job-card {
  background: var(--gray);
  border-left: 4px solid var(--blue);
  border-radius: 8px;
  padding: 8px 10px;
  margin: 5px 4px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.06);
  font-size: 0.86rem;
  word-wrap: break-word;
  overflow-wrap: break-word;
  white-space: normal;
}
.job-card b {
  display: block;
  font-weight: 700;
  margin-bottom: 3px;
  line-height: 1.3;
}
.job-card span {
  display: block;
  font-size: 0.78rem;
  color: #444;
}

/* ======= RESPONSIVIDADE ======= */
@media (max-width: 1500px) { .block-container { zoom: 0.9; } }
@media (max-width: 1200px) { .block-container { zoom: 0.8; } }
</style>
""", unsafe_allow_html=True)

# ===========================================================
# DADOS E FILTROS
# ===========================================================
data = load_excel_data()
df = data.get("job_profile", pd.DataFrame())

required_cols = ["Job Family","Sub Job Family","Job Profile","Career Path","Global Grade"]
missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error(f"Colunas ausentes: {', '.join(missing)}")
    st.stop()

df = df.dropna(subset=["Job Family","Sub Job Family","Job Profile","Global Grade"])
df["Global Grade"] = df["Global Grade"].astype(str).str.replace(r"\.0$","",regex=True)

# ===========================================================
# TOPO FIXO: TÍTULO E FILTROS
# ===========================================================
st.markdown("<div class='topbar'>", unsafe_allow_html=True)
section("🗺️ Job Map")

col1, col2 = st.columns([2, 2])
families = ["Todas"] + sorted(df["Job Family"].dropna().unique().tolist())
paths = ["Todas"] + sorted(df["Career Path"].dropna().unique().tolist())
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
# MAPAS DE FAMÍLIA E SUBFAMÍLIA
# ===========================================================
familias = sorted(df["Job Family"].unique().tolist())
cores_familia = [
    "#7b6c7f", "#4B5A73", "#857160", "#607d8b", "#6E7065",
    "#5b6c80", "#708090", "#786d8b", "#6d706f", "#837567"
]
cores_claras = [
    "#ece9ed", "#e8ebf2", "#f0ebe6", "#edf2f4", "#f1f2f0",
    "#edf2f7", "#f1f0ec", "#efedf3", "#f2f0ed", "#edeef0"
]
map_cor_fam = {f: cores_familia[i % len(cores_familia)] for i, f in enumerate(familias)}
map_cor_sub = {f: cores_claras[i % len(cores_claras)] for i, f in enumerate(familias)}

subfamilias = {
    f: sorted(df[df["Job Family"] == f]["Sub Job Family"].dropna().unique().tolist())
    for f in familias
}

grades = sorted(df["Global Grade"].unique(), key=lambda x: int(x) if x.isdigit() else 999, reverse=True)

# ===========================================================
# DIMENSÕES DAS COLUNAS
# ===========================================================
def largura(text):
    base = len(str(text))
    return min(max(200, base * 9 + 40), 420)

colunas = ["160px"]
for f in familias:
    for sf in subfamilias[f]:
        maior = max([sf] + df[(df["Job Family"] == f) & (df["Sub Job Family"] == sf)]["Job Profile"].tolist(), key=len)
        colunas.append(f"{largura(maior)}px")
grid_template = f"grid-template-columns: {' '.join(colunas)};"

# ===========================================================
# HTML FINAL
# ===========================================================
html = ["<div class='map-wrapper'>"]
html.append(f"<div class='jobmap-grid' style='{grid_template}'>")

# Linha 1 — GG + Famílias
html.append("<div class='gg-header'>GG</div>")
for f in familias:
    span = len(subfamilias[f])
    html.append(f"<div class='header-family' style='grid-column: span {span}; background:{map_cor_fam[f]};'>{f}</div>")

# Linha 2 — Subfamílias
for f in familias:
    for sf in subfamilias[f]:
        html.append(f"<div class='header-subfamily' style='background:{map_cor_sub[f]};'>{sf}</div>")

# Demais linhas (Grades + Cards)
for g in grades:
    html.append(f"<div class='gg-cell'>GG {g}</div>")
    for f in familias:
        fam_df = df[df["Job Family"] == f]
        for sf in subfamilias[f]:
            cell = fam_df[(fam_df["Sub Job Family"] == sf) & (fam_df["Global Grade"] == g)]
            if cell.empty:
                html.append("<div class='cell'></div>")
            else:
                cards = "".join([
                    f"<div class='job-card'><b>{r['Job Profile']}</b><span>{r['Career Path']}</span></div>"
                    for _, r in cell.iterrows()
                ])
                html.append(f"<div class='cell'>{cards}</div>")

html.append("</div></div>")
st.markdown("".join(html), unsafe_allow_html=True)
