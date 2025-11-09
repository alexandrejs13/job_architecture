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
  --gray-line: #dadada;
  --gray-bg: #f8f9fa;
  --dark-gray: #73706d;
}

/* ======= BLOCO PRINCIPAL ======= */
.block-container {
  max-width: 1750px !important;
  margin: 0 auto !important;
  padding: 2.5rem 1.5rem 2rem 1.5rem !important;
}

/* ======= CABEÇALHO FIXO ======= */
.topbar {
  position: sticky;
  top: 0;
  z-index: 200;
  background: white;
  padding: 10px 0 5px 0;
  border-bottom: 2px solid var(--blue);
}
h1 {
  color: var(--blue);
  font-weight: 900 !important;
  font-size: 1.9rem !important;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px !important;
}

/* ======= ÁREA DE MAPA ======= */
.map-wrapper {
  height: 78vh;
  overflow: auto;
  border-top: 3px solid var(--blue);
  border-bottom: 3px solid var(--blue);
  background: white;
  position: relative;
  white-space: nowrap;
}

/* ======= GRID PRINCIPAL ======= */
.jobmap-grid {
  display: grid;
  border-collapse: collapse;
  width: max-content;
  font-size: 0.88rem;
  border-right: 1px solid var(--gray-line);
  border-bottom: 1px solid var(--gray-line);
}
.jobmap-grid > div {
  border: 1px solid var(--gray-line);
  box-sizing: border-box;
}

/* ======= CABEÇALHOS ======= */
.header-family {
  font-weight: 800;
  color: #fff;
  padding: 12px 10px;
  text-align: center;
  background: var(--dark-gray);
  border-right: 1px solid white;
  position: sticky;
  top: 0;
  z-index: 55;
  white-space: normal;
  line-height: 1.3;
}
.header-subfamily {
  font-weight: 600;
  background: var(--gray-bg);
  padding: 10px;
  text-align: center;
  border-right: 1px solid var(--gray-line);
  position: sticky;
  top: 52px;
  z-index: 54;
  white-space: normal;
  border-top: none !important; /* remove linha fantasma */
}

/* ======= COLUNA GG ======= */
.gg-header {
  background: #000;
  color: white;
  font-weight: 800;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  grid-row: span 2;
  position: sticky;
  top: 0;
  left: 0;
  z-index: 100 !important;
  border-right: 2px solid white;
}
.gg-cell {
  background: #000;
  color: white;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  position: sticky;
  left: 0;
  z-index: 90 !important;
  border-right: 2px solid white;
  border-top: 1px solid white;
}

/* ======= CÉLULAS ======= */
.cell {
  background: white;
  padding: 8px;
  text-align: left;
  min-height: 70px;
  vertical-align: middle;
}
.job-card {
  background: #f9f9f9;
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
  margin-bottom: 2px;
  line-height: 1.3;
}
.job-card span {
  display: block;
  font-size: 0.78rem;
  color: #444;
}

/* ======= Sombra vertical entre GG e Families ======= */
.gg-header::after, .gg-cell::after {
  content: "";
  position: absolute;
  right: -2px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(to right, rgba(255,255,255,0.2), rgba(0,0,0,0.15));
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

required = ["Job Family", "Sub Job Family", "Job Profile", "Career Path", "Global Grade"]
missing = [c for c in required if c not in df.columns]
if missing:
    st.error(f"Colunas ausentes: {', '.join(missing)}")
    st.stop()

df = df.dropna(subset=["Job Family", "Sub Job Family", "Job Profile", "Global Grade"])
df["Global Grade"] = df["Global Grade"].astype(str).str.replace(r"\\.0$", "", regex=True)

# ===========================================================
# FILTROS E CABEÇALHO
# ===========================================================
st.markdown("<div class='topbar'>", unsafe_allow_html=True)
section("🗺️ Job Map")
col1, col2 = st.columns([2, 2])

families_order = [
    "Top Executive/General Management", "Corporate Affairs/Communications",
    "Legal & Internal Audit", "Finance", "IT", "People & Culture",
    "Sales", "Marketing", "Technical Services", "Research & Development",
    "Technical Engineering", "Operations", "Supply Chain & Logistics",
    "Quality Management", "Facility & Administrative Services"
]
families = ["Todas"] + [f for f in families_order if f in df["Job Family"].unique()]
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
# ESTRUTURA DE GRID
# ===========================================================
familias = [f for f in families_order if f in df["Job Family"].unique()]
cores_familia = [
    "#4B4B4B", "#5E5D74", "#6D6268", "#5B686F", "#626A5E",
    "#5C5E77", "#6E5F70", "#676E6F", "#707075", "#5F5D68",
    "#605F67", "#6E6B6C", "#67686A", "#5E5E5E", "#646363"
]
cores_sub = ["#EDEDED" for _ in cores_familia]
map_cor_fam = {f: cores_familia[i % len(cores_familia)] for i, f in enumerate(familias)}
map_cor_sub = {f: cores_sub[i % len(cores_sub)] for i, f in enumerate(familias)}

subfamilias = {
    f: sorted(df[df["Job Family"] == f]["Sub Job Family"].dropna().unique().tolist())
    for f in familias
}
grades = sorted(df["Global Grade"].unique(), key=lambda x: int(x) if x.isdigit() else 999, reverse=True)

# ===========================================================
# DIMENSÕES
# ===========================================================
def largura(t):
    return min(max(220, len(str(t)) * 8 + 50), 420)

colunas = ["160px"]
for f in familias:
    for sf in subfamilias[f]:
        maior = max([sf] + df[(df["Job Family"] == f) & (df["Sub Job Family"] == sf)]["Job Profile"].tolist(), key=len)
        colunas.append(f"{largura(maior)}px")
grid_template = f"grid-template-columns: {' '.join(colunas)};"

# ===========================================================
# HTML DO GRID
# ===========================================================
html = ["<div class='map-wrapper'><div class='jobmap-grid' style='{grid_template}'>".format(grid_template=grid_template)]

# Linha 1 — Famílias
html.append("<div class='gg-header'>GG</div>")
for f in familias:
    span = len(subfamilias[f])
    html.append(f"<div class='header-family' style='grid-column: span {span}; background:{map_cor_fam[f]};'>{f}</div>")

# Linha 2 — Subfamílias
for f in familias:
    for sf in subfamilias[f]:
        html.append(f"<div class='header-subfamily' style='background:{map_cor_sub[f]};'>{sf}</div>")

# Demais linhas (Grades + Cargos)
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

# ===========================================================
# VISUALIZAÇÃO INTERATIVA (🔍 ⬇️ ⛶)
# ===========================================================
st.divider()
st.caption("Visualização interativa (zoom, download e tela cheia disponíveis abaixo):")
st.dataframe(df[["Job Family", "Sub Job Family", "Job Profile", "Career Path", "Global Grade"]],
             use_container_width=True, height=450)
