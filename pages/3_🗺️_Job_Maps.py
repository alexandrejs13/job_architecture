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
  --green: #28a745;
  --orange: #fd7e14;
  --purple: #6f42c1;
  --gray-line: #dadada;
  --gray-bg: #f8f9fa;
  --dark-gray: #333333;
}

/* === CONTAINER GERAL === */
.block-container {
  max-width: 95% !important;
  margin: 0 auto !important;
  padding: 1.5rem 3rem !important; /* mais espaçamento lateral */
}

/* === TOPO E CABEÇALHO === */
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

/* === BOTÃO DE TELA CHEIA === */
.fullscreen-btn {
  background-color: var(--blue);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 6px 14px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  margin-top: 22px;
}
.fullscreen-btn:hover {
  background-color: #0d47c3;
}

/* === MAPA E GRID === */
.map-wrapper {
  height: 78vh;
  overflow: auto;
  border-top: 3px solid var(--blue);
  border-bottom: 3px solid var(--blue);
  background: white;
  position: relative;
  will-change: transform;
  box-shadow: 0 0 15px rgba(0,0,0,0.05);
  margin: 0 auto;
  max-width: 1800px;
}

.jobmap-grid {
  display: grid;
  border-collapse: collapse;
  width: max-content;
  font-size: 0.88rem;
  grid-template-rows: 50px 45px repeat(auto-fill, 110px) !important;
  grid-auto-rows: 110px !important;
  align-content: start !important;
  background-color: white !important;
  margin: 0 auto;
}

.jobmap-grid > div {
  background-color: white;
  border-right: 1px solid var(--gray-line);
  border-bottom: 1px solid var(--gray-line);
  box-sizing: border-box;
}

/* === CABEÇALHOS === */
.header-family {
  font-weight: 800;
  color: #fff;
  padding: 0 5px;
  text-align: center;
  border-right: 1px solid rgba(255,255,255,0.3) !important;
  border-bottom: 0 !important;
  margin-bottom: 0;
  position: sticky;
  top: 0;
  z-index: 57;
  white-space: normal;
  height: 50px !important;
  display: flex;
  align-items: center;
  justify-content: center;
}
.header-subfamily {
  font-weight: 600;
  padding: 0 5px;
  text-align: center;
  position: sticky;
  top: 50px;
  z-index: 56;
  border-top: 0 !important;
  height: 45px !important;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* === COLUNA GG === */
.gg-header {
  background: #000 !important;
  color: white;
  font-weight: 800;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  grid-row: 1 / span 2;
  position: sticky;
  left: 0;
  top: 0;
  z-index: 60;
  border-right: 2px solid white !important;
  height: 95px !important;
}
.gg-cell {
  background: #000 !important;
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
  font-size: 0.9rem;
}

/* === CELULAS E CARDS === */
.cell {
  background: white !important;
  padding: 8px;
  text-align: left;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  justify-content: center;
}

.job-card {
  background: #f9f9f9;
  border-left-width: 5px;
  border-left-style: solid;
  border-radius: 6px;
  padding: 6px 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  font-size: 0.75rem;
  width: 135px;
  height: 75px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  transition: all 0.2s ease-in-out;
}
.job-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}
.job-card b {
  display: block;
  font-weight: 700;
  margin-bottom: 3px;
  color: #222;
  overflow: hidden;
}
.job-card span {
  display: block;
  font-size: 0.7rem;
  color: #666;
  line-height: 1.1;
}

/* === EFEITO DE SOMBRA NA COLUNA GG === */
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
</style>
""", unsafe_allow_html=True)

# ===========================================================
# DADOS
# ===========================================================
data = load_excel_data()
df = data.get("job_profile", pd.DataFrame())

required = ["Job Family", "Sub Job Family", "Job Profile", "Career Path", "Global Grade"]
for col in required:
    df[col] = df[col].astype(str).str.strip()

df = df[~df["Job Family"].isin(["nan", "None", ""])]
df = df[~df["Job Profile"].isin(["nan", "None", ""])]
df = df[~df["Global Grade"].isin(["nan", "None", ""])]
df["Global Grade"] = df["Global Grade"].str.replace(r"\\.0$", "", regex=True)

# ===========================================================
# FILTROS + BOTÃO DE TELA CHEIA
# ===========================================================
st.markdown("<div class='topbar'>", unsafe_allow_html=True)
section("🗺️ Job Map")

col1, col2, col3 = st.columns([2, 2, 0.6])  # terceira coluna reservada ao botão

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

if family_filter != "Todas":
    available_paths = df[df["Job Family"] == family_filter]["Career Path"].unique().tolist()
else:
    available_paths = df["Career Path"].unique().tolist()
paths_options = ["Todas"] + sorted([p for p in available_paths if pd.notna(p) and p != 'nan' and p != ''])

with col2:
    path_filter = st.selectbox("Trilha de Carreira", paths_options)

# --- Botão de tela cheia / voltar ---
with col3:
    fullscreen = st.button("🖥️ Tela Cheia", key="fullscreen_toggle")

st.markdown("</div>", unsafe_allow_html=True)

# ===========================================================
# VISUALIZAÇÃO NORMAL / TELA CHEIA
# ===========================================================
if fullscreen:
    st.session_state["fullscreen"] = not st.session_state.get("fullscreen", False)

fullscreen_mode = st.session_state.get("fullscreen", False)
if fullscreen_mode:
    st.markdown("<style>header, .stApp > div:first-child {display:none !important;}</style>", unsafe_allow_html=True)
    st.button("⬅️ Voltar", key="exit_full", on_click=lambda: st.session_state.update({"fullscreen": False}))
    st.markdown("<h3 style='text-align:center; color:#145efc;'>🗺️ Modo Tela Cheia</h3>", unsafe_allow_html=True)

# ===========================================================
# MAPA ESTRUTURADO (mantém igual ao seu código)
# ===========================================================
# ... (daqui pra baixo, mantenha exatamente o mesmo conteúdo que você já tem — grid, cores, células, etc.)
