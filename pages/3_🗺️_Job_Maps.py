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
# CSS COMPLETO (COM CORREÇÃO DA LINHA BRANCA)
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
  grid-auto-rows: minmax(60px, auto);
  row-gap: 0 !important; /* Garante zero espaço entre linhas */
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
  /* REMOVE A BORDA INFERIOR PARA NÃO TER LINHA BRANCA */
  border-bottom: none !important;
  margin-bottom: 0 !important;
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
  /* GARANTE QUE NÃO TENHA BORDA SUPERIOR */
  border-top: none !important;
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

.cell {
  background: white;
  padding: 8px;
  text-align: left;
  vertical-align: middle;
  z-index: 1;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  align-content: center;
}

.job-card {
  background: #f9f9f9;
  border-left: 4px solid var(--blue);
  border-radius: 6px;
  padding: 6px 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  font-size: 0.75rem;
  word-wrap: break-word;
  overflow-wrap: break-word;
  white-space: normal;
  width: 135px;
  height: 75px;
  flex: 0 0 135px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  overflow: hidden;
}
.job-card b {
  display: block;
  font-weight: 700;
  margin-bottom: 3px;
  line-height: 1.15;
  color: #222;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.job-card span {
  display: block;
  font-size: 0.7rem;
  color: #666;
  line-height: 1.1;
  margin-top: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
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
# FILTROS DEPENDENTES
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

if family_filter != "
