import streamlit as st
import pandas as pd
from utils.data_loader import load_excel_tables

st.set_page_config(layout="wide", page_title="🏗️ Structure Level")
st.markdown("## 🏗️ Structure Level")

DATA = load_excel_tables()
if "level_structure" not in DATA:
    st.error("❌ Não encontrei `data/Level Structure.xlsx`.")
    st.stop()

df = DATA["level_structure"].copy()

# Tenta ordenar por grade quando existir
if "Global Grade" in df.columns:
    df["__gg_sort__"] = df["Global Grade"].astype(str).str.extract(r"(\d+)").fillna("0").astype(int)
else:
    df["__gg_sort__"] = 0

# Filtros amigáveis
cols_possible = {
    "Career Path": "Career Path",
    "Structure Level": "Structure Level",
    "Level Name": "Level Name",
    "Level Description": "Level Description",
    "Global Grade": "Global Grade",
}
present = [c for c in cols_possible.values() if c in df.columns]

col1, col2 = st.columns([2, 2])
with col1:
    if "Career Path" in df.columns:
        paths = ["Todas"] + sorted(df["Career Path"].dropna().unique().tolist())
        sel_path = st.selectbox("Trilha de Carreira", paths)
    else:
        sel_path = "Todas"
with col2:
    if "Structure Level" in df.columns:
        levels = ["Todos"] + sorted(df["Structure Level"].dropna().unique().tolist())
        sel_level = st.selectbox("Nível (Structure Level)", levels)
    else:
        sel_level = "Todos"

view = df.copy()
if sel_path != "Todas" and "Career Path" in view.columns:
    view = view[view["Career Path"] == sel_path]
if sel_level != "Todos" and "Structure Level" in view.columns:
    view = view[view["Structure Level"] == sel_level]

view = view.sort_values(by=["Career Path", "Structure Level", "__gg_sort__"], ascending=[True, True, False], na_position="last")

# Mostra só colunas relevantes se existirem
show_cols = [c for c in ["Career Path", "Structure Level", "Level Name", "Level Description", "Global Grade"] if c in view.columns]
if not show_cols:
    st.warning("Exibindo planilha completa (não encontrei colunas padrão).")
    st.dataframe(view, use_container_width=True, hide_index=True)
else:
    st.dataframe(view[show_cols], use_container_width=True, hide_index=True)
