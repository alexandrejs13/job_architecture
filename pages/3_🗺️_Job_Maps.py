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
# CSS COMPLETO (CARDS MENORES E PADRONIZADOS)
# ===========================================================
st.markdown("""
<style>
:root {
  --blue: #145efc;
  --gray-line: #dadada;
  --gray-bg: #f8f9fa;
  --dark-gray: #73706d;
}

.block-container {
  max-width: 100% !important;
  margin: 0 !important;
  padding: 1rem 2rem !important;
}

.topbar {
  position: sticky;
  top: 0;
  z-index: 200;
  background: white;
  padding: 10px 0 5px 0;
  border-bottom: 2px solid var(--blue);
  margin-bottom: 15px;
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

.map-wrapper {
  height: 78vh;
  overflow: auto;
  border-top: 3px solid var(--blue);
  border-bottom: 3px solid var(--blue);
  background: white;
  position: relative;
  will-change: transform;
  box-shadow: 0 0 15px rgba(0,0,0,0.05);
}

.jobmap-grid {
  display: grid;
  border-collapse: collapse;
  width: max-content;
  font-size: 0.88rem;
  grid-auto-rows: minmax(60px, auto); /* Altura mínima da linha reduzida */
}

.jobmap-grid > div {
  border-right: 1px solid var(--gray-line);
  border-bottom: 1px solid var(--gray-line);
  box-sizing: border-box;
}

.header-family {
  font-weight: 800;
  color: #fff;
  padding: 10px 5px;
  text-align: center;
  background: var(--dark-gray);
  border-right: 1px solid white !important;
  position: sticky;
  top: 0;
  z-index: 55;
  white-space: normal;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  grid-row: 1;
  font-size: 0.9rem;
}

.header-subfamily {
  font-weight: 600;
  background: var(--gray-bg);
  padding: 8px 5px;
  text-align: center;
  position: sticky;
  top: 50px;
  z-index: 55;
  white-space: normal;
  border-bottom: 2px solid var(--gray-line) !important;
  min-height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  grid-row: 2;
  font-size: 0.85rem;
}

.gg-header {
  background: #000;
  color: white;
  font-weight: 800;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  grid-row: 1 / span 2;
  grid-column: 1;
  position: sticky;
  left: 0;
  top: 0;
  z-index: 60;
  border-right: 2px solid white !important;
  border-bottom: 2px solid var(--gray-line) !important;
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
  z-index: 55;
  border-right: 2px solid white !important;
  border-top: 1px solid white !important;
  grid-column: 1;
  font-size: 0.9rem;
}

/* === CÉLULAS (LAYOUT FLEX) === */
.cell {
  background: white;
  padding: 6px;
  text-align: left;
  vertical-align: middle;
  z-index: 1;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 6px;
  align-items: flex-start;
  align-content: center;
}

/* === CARDS PADRONIZADOS E MENORES === */
.job-card {
  background: #f9f9f9;
  border-left: 3px solid var(--blue);
  border-radius: 4px;
  padding: 5px 6px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.08);
  font-size: 0.75rem; /* Fonte menor */
  word-wrap: break-word;
  overflow-wrap: break-word;
  white-space: normal;
  
  /* Tamanho fixo e padronizado */
  width: 125px;
  flex: 0 0 125px; /* Não cresce nem diminui, fica sempre com 125px */
  min-height: 45px; /* Altura mínima para uniformidade visual */
}
.job-card b {
  display: block;
  font-weight: 700;
  margin-bottom: 2px;
  line-height: 1.1;
  color: #222;
}
.job-card span {
  display: block;
  font-size: 0.7rem;
  color: #666;
  line-height: 1;
}

.gg-header::after, .gg-cell::after {
  content: "";
  position: absolute;
  right: -5px;
  top: 0;
  bottom: 0;
  width: 5px;
  background: linear-gradient(to right, rgba(0,0,0,0.15), transparent);
  pointer-events: none;
}

@media (max-width: 1500px) { .block-container { zoom: 0.9; } }
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

for col in required:
    df[col] = df[col].astype(str).str.strip()

df["Sub Job Family"] = df["Sub Job Family"].replace(['nan', 'None', '', '<NA>'], '-')
df = df[~df["Job Family"].isin(['nan', 'None', ''])]
df = df[~df["Job Profile"].isin(['nan', 'None', ''])]
df = df[~df["Global Grade"].isin(['nan', 'None', ''])]
df["Global Grade"] = df["Global Grade"].str.replace(r"\.0$", "", regex=True)

# ===========================================================
# FILTROS
# ===========================================================
st.markdown("<div class='topbar'>", unsafe_allow_html=True)
section("🗺️ Job Map")
col1, col2 = st.columns([2, 2])

preferred_order = [
    "Top Executive/General Management", "Corporate Affairs/Communications", "Legal & Internal Audit",
    "Finance", "IT", "People & Culture", "Sales", "Marketing", "Technical Services",
    "Research & Development", "Technical Engineering", "Operations", "Supply Chain & Logistics",
    "Quality Management", "Facility & Administrative Services"
]

existing_families = set(df["Job Family"].unique())
families_order = [f for f in preferred_order if f in existing_families]
families_order.extend(sorted(list(existing_families - set(families_order))))

with col1:
    family_filter = st.selectbox("Família", ["Todas"] + families_order)
with col2:
    path_filter = st.selectbox("Trilha de Carreira", ["Todas"] + sorted(df["Career Path"].unique().tolist()))
st.markdown("</div>", unsafe_allow_html=True)

if family_filter != "Todas":
    df = df[df["Job Family"] == family_filter]
if path_filter != "Todas":
    df = df[df["Career Path"] == path_filter]

if df.empty:
    st.warning("Nenhum cargo encontrado.")
    st.stop()

# ===========================================================
# PREPARAÇÃO DO GRID
# ===========================================================
active_families = [f for f in families_order if f in df["Job Family"].unique()]
grades = sorted(df["Global Grade"].unique(), key=lambda x: int(x) if x.isdigit() else 999, reverse=True)

subfamilias_map = {}
col_index = 2
header_spans = {}

for f in active_families:
    subs = sorted(df[df["Job Family"] == f]["Sub Job Family"].unique().tolist())
    header_spans[f] = len(subs)
    for sf in subs:
        subfamilias_map[(f, sf)] = col_index
        col_index += 1

content_map = {}
cell_html_cache = {}
cards_count_map = {}

for g in grades:
    for (f, sf), c_idx in subfamilias_map.items():
        cell_df = df[(df["Job Family"] == f) & (df["Sub Job Family"] == sf) & (df["Global Grade"] == g)]
        count = len(cell_df)
        cards_count_map[(g, c_idx)] = count

        if count == 0:
            content_map[(g, c_idx)] = None
            continue
        
        jobs_sig = "|".join(sorted((cell_df["Job Profile"] + cell_df["Career Path"]).unique()))
        content_map[(g, c_idx)] = jobs_sig
        
        cards_html = "".join([
            f"<div class='job-card'><b>{row['Job Profile']}</b><span>{row['Career Path']}</span></div>"
            for _, row in cell_df.iterrows()
        ])
        cell_html_cache[(g, c_idx)] = cards_html

span_map = {}
skip_set = set()
for (_, c_idx) in subfamilias_map.items():
    for i, g in enumerate(grades):
        if (g, c_idx) in skip_set: continue
        current_sig = content_map.get((g, c_idx))
        if current_sig is None:
            span_map[(g, c_idx)] = 1
            continue
        span = 1
        for next_g in grades[i+1:]:
            if content_map.get((next_g, c_idx)) == current_sig:
                span += 1
                skip_set.add((next_g, c_idx))
            else:
                break
        span_map[(g, c_idx)] = span

# ===========================================================
# CÁLCULO DE LARGURAS
# ===========================================================
def largura_texto(text):
    return len(str(text)) * 7 + 30 # Reduzido ligeiramente o multiplicador de texto

col_widths = ["100px"] # Coluna GG um pouco menor

for (f, sf), c_idx in subfamilias_map.items():
    cargos = df[(df["Job Family"] == f) & (df["Sub Job Family"] == sf)]["Job Profile"].tolist()
    maior_texto = max([sf] + cargos if cargos else [sf], key=len)
    width_by_text = largura_texto(maior_texto)
    
    max_cards_in_col = 0
    for g in grades:
        max_cards_in_col = max(max_cards_in_col, cards_count_map.get((g, c_idx), 0))
    
    # Ajustado para 135px por card (125px width + 10px gap aprox)
    width_by_cards = min(max_cards_in_col, 3) * 135
    
    final_width = max(180, width_by_text, width_by_cards) # Mínimo reduzido para 180px
    col_widths.append(f"{final_width}px")

grid_template = f"grid-template-columns: {' '.join(col_widths)};"

cores_fam = ["#726C5B", "#5F6A73", "#6F5C60", "#5D6E70", "#6B715B", "#5B5F77", "#725E7A", "#666C5B", "#736A65", "#6C5F70", "#655C6F", "#6A6C64", "#6C6868", "#5F7073", "#70685E"]
cores_sub = ["#EDEBE8", "#ECEEF0", "#F2ECEF", "#EEF2F2", "#F0F2ED", "#EDEDF3", "#F1EEF4", "#F1F2EE", "#F2EFED", "#EFEFF2", "#EFEDED", "#EFEFEF", "#F2F2F0", "#EFEFEF", "#EEEFEF"]
map_cor_fam = {f: cores_fam[i % len(cores_fam)] for i, f in enumerate(families_order)}
map_cor_sub = {f: cores_sub[i % len(cores_sub)] for i, f in enumerate(families_order)}

# ===========================================================
# RENDERIZAÇÃO
# ===========================================================
html = ["<div class='map-wrapper'><div class='jobmap-grid' style='{grid_template}'>".format(grid_template=grid_template)]
html.append("<div class='gg-header'>GG</div>")

current_col = 2
for f in active_families:
    span = header_spans[f]
    html.append(f"<div class='header-family' style='grid-column: {current_col} / span {span}; background:{map_cor_fam[f]};'>{f}</div>")
    current_col += span

for (f, sf), c_idx in subfamilias_map.items():
    html.append(f"<div class='header-subfamily' style='grid-column: {c_idx}; background:{map_cor_sub[f]};'>{sf}</div>")

for i, g in enumerate(grades):
    row_idx = i + 3
    html.append(f"<div class='gg-cell' style='grid-row: {row_idx};'>GG {g}</div>")
    for (f, sf), c_idx in subfamilias_map.items():
        if (g, c_idx) in skip_set: continue
        span = span_map.get((g, c_idx), 1)
        row_str = f"grid-row: {row_idx} / span {span};" if span > 1 else f"grid-row: {row_idx};"
        html.append(f"<div class='cell' style='grid-column: {c_idx}; {row_str}'>{cell_html_cache.get((g, c_idx), '')}</div>")

html.append("</div></div>")
st.markdown("".join(html), unsafe_allow_html=True)
