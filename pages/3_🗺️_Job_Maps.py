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
# CSS COMPLETO (CONGELAMENTO + AJUSTES VISUAIS)
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
  padding: 0 !important;
}

/* ======= CABEÇALHO FIXO (TOPBAR) ======= */
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
  will-change: transform; /* Melhora performance do scroll sticky */
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

/* ======= CABEÇALHOS (LINHA 1 - FAMÍLIAS) ======= */
.header-family {
  font-weight: 800;
  color: #fff;
  padding: 12px 10px;
  text-align: center;
  background: var(--dark-gray);
  border-right: 1px solid white;
  border-bottom: none;
  position: sticky;
  top: 0;
  z-index: 55;
  white-space: normal;
  height: 55px; /* Altura fixa para garantir alinhamento */
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ======= CABEÇALHOS (LINHA 2 - SUBFAMÍLIAS) ======= */
.header-subfamily {
  font-weight: 600;
  background: var(--gray-bg);
  padding: 10px;
  text-align: center;
  border-right: 1px solid var(--gray-line);
  border-top: none;
  position: sticky;
  top: 55px; /* Começa exatamente onde a linha 1 termina */
  z-index: 55;
  white-space: normal;
  border-bottom: 2px solid var(--gray-line) !important;
  height: auto;
  min-height: 45px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ======= COLUNA GG (CANTO SUPERIOR ESQUERDO) ======= */
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
  left: 0;
  top: 0;
  z-index: 60; /* O mais alto para ficar no canto */
  border-right: 2px solid white;
  border-bottom: 2px solid var(--gray-line);
}

/* ======= CÉLULAS DA COLUNA GG (ESQUERDA) ======= */
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
  border-right: 2px solid white;
  border-top: 1px solid white;
}

/* ======= CÉLULAS DE CONTEÚDO ======= */
.cell {
  background: white;
  padding: 8px;
  text-align: left;
  min-height: 80px;
  vertical-align: middle;
  z-index: 1;
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

/* ======= Sombra vertical para profundidade ======= */
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

/* ======= RESPONSIVIDADE ======= */
@media (max-width: 1500px) { .block-container { zoom: 0.9; } }
@media (max-width: 1200px) { .block-container { zoom: 0.8; } }
</style>
""", unsafe_allow_html=True)

# ===========================================================
# DADOS E LIMPEZA
# ===========================================================
data = load_excel_data()
df = data.get("job_profile", pd.DataFrame())

required = ["Job Family", "Sub Job Family", "Job Profile", "Career Path", "Global Grade"]
missing = [c for c in required if c not in df.columns]
if missing:
    st.error(f"Colunas ausentes: {', '.join(missing)}")
    st.stop()

# 1. Limpeza de espaços em branco
for col in required:
    df[col] = df[col].astype(str).str.strip()

# 2. Tratamento de nulos críticos (evita perder Executivos sem subfamília)
df["Sub Job Family"] = df["Sub Job Family"].replace(['nan', 'None', '', '<NA>'], '-')

# 3. Filtragem de linhas inválidas
df = df[~df["Job Family"].isin(['nan', 'None', ''])]
df = df[~df["Job Profile"].isin(['nan', 'None', ''])]
df = df[~df["Global Grade"].isin(['nan', 'None', ''])]

# 4. Normalização do Grade
df["Global Grade"] = df["Global Grade"].str.replace(r"\.0$", "", regex=True)

# ===========================================================
# FILTROS E CABEÇALHO
# ===========================================================
st.markdown("<div class='topbar'>", unsafe_allow_html=True)
section("🗺️ Job Map")
col1, col2 = st.columns([2, 2])

# Ordem preferencial das famílias
preferred_order = [
    "Top Executive/General Management",
    "Corporate Affairs/Communications",
    "Legal & Internal Audit",
    "Finance",
    "IT",
    "People & Culture",
    "Sales",
    "Marketing",
    "Technical Services",
    "Research & Development",
    "Technical Engineering",
    "Operations",
    "Supply Chain & Logistics",
    "Quality Management",
    "Facility & Administrative Services"
]

# Garante que usamos apenas famílias que existem nos dados
existing_families = set(df["Job Family"].unique())
families_order = [f for f in preferred_order if f in existing_families]
# Adiciona outras famílias que possam existir no Excel mas não na lista preferencial
families_order.extend(sorted(list(existing_families - set(families_order))))

families_options = ["Todas"] + families_order
paths_options = ["Todas"] + sorted(df["Career Path"].unique().tolist())

with col1:
    family_filter = st.selectbox("Família", families_options)
with col2:
    path_filter = st.selectbox("Trilha de Carreira", paths_options)
st.markdown("</div>", unsafe_allow_html=True)

# APLICAÇÃO DOS FILTROS
if family_filter != "Todas":
    df = df[df["Job Family"] == family_filter]
if path_filter != "Todas":
    df = df[df["Career Path"] == path_filter]

if df.empty:
    st.warning("Nenhum cargo encontrado com os filtros selecionados.")
    st.stop()

# ===========================================================
# PREPARAÇÃO DO GRID (BASEADO NOS DADOS FILTRADOS)
# ===========================================================
# Define as famílias ativas com base no dataframe JÁ FILTRADO
active_families = [f for f in families_order if f in df["Job Family"].unique()]

cores_familia = [
    "#726C5B", "#5F6A73", "#6F5C60", "#5D6E70", "#6B715B",
    "#5B5F77", "#725E7A", "#666C5B", "#736A65", "#6C5F70",
    "#655C6F", "#6A6C64", "#6C6868", "#5F7073", "#70685E"
]
cores_sub = [
    "#EDEBE8", "#ECEEF0", "#F2ECEF", "#EEF2F2", "#F0F2ED",
    "#EDEDF3", "#F1EEF4", "#F1F2EE", "#F2EFED", "#EFEFF2",
    "#EFEDED", "#EFEFEF", "#F2F2F0", "#EFEFEF", "#EEEFEF"
]
map_cor_fam = {f: cores_familia[i % len(cores_familia)] for i, f in enumerate(families_order)}
map_cor_sub = {f: cores_sub[i % len(cores_sub)] for i, f in enumerate(families_order)}

subfamilias = {
    f: sorted(df[df["Job Family"] == f]["Sub Job Family"].unique().tolist())
    for f in active_families
}
# Ordenação numérica decrescente para os Grades
grades = sorted(df["Global Grade"].unique(), key=lambda x: int(x) if x.isdigit() else 999, reverse=True)

# ===========================================================
# CÁLCULO DE DIMENSÕES
# ===========================================================
def largura(text):
    # Ajuste fino na largura das colunas baseado no tamanho do texto
    return min(max(220, len(str(text)) * 8 + 50), 420)

colunas_css = ["120px"] # Largura fixa da coluna GG
for f in active_families:
    for sf in subfamilias[f]:
        # Encontra o maior texto (seja o nome da subfamília ou de um cargo nela)
        cargos_na_sub = df[(df["Job Family"] == f) & (df["Sub Job Family"] == sf)]["Job Profile"].tolist()
        maior_texto = max([sf] + cargos_na_sub if cargos_na_sub else [sf], key=len)
        colunas_css.append(f"{largura(maior_texto)}px")

grid_template = f"grid-template-columns: {' '.join(colunas_css)};"

# ===========================================================
# GERAÇÃO DO HTML
# ===========================================================
html = ["<div class='map-wrapper'><div class='jobmap-grid' style='{grid_template}'>".format(grid_template=grid_template)]

# --- Linha 1: Cabeçalhos das Famílias ---
html.append("<div class='gg-header'>GG</div>")
for f in active_families:
    span = len(subfamilias[f])
    html.append(f"<div class='header-family' style='grid-column: span {span}; background:{map_cor_fam[f]};'>{f}</div>")

# --- Linha 2: Cabeçalhos das Subfamílias ---
for f in active_families:
    for sf in subfamilias[f]:
        html.append(f"<div class='header-subfamily' style='background:{map_cor_sub[f]};'>{sf}</div>")

# --- Demais linhas: Grades + Cargos ---
for g in grades:
    html.append(f"<div class='gg-cell'>GG {g}</div>")
    for f in active_families:
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
