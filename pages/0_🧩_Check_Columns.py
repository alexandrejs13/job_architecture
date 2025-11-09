import streamlit as st
import pandas as pd
from utils.data_loader import load_excel_tables

st.set_page_config(layout="centered", page_title="🧩 Column Check")

st.title("🧩 Diagnóstico de Colunas do Excel")

DATA = load_excel_tables()

if "job_profile" in DATA:
    jp = DATA["job_profile"]
    st.subheader("📘 Job Profile.xlsx — Colunas encontradas")
    st.dataframe(pd.DataFrame({"Column": jp.columns}), hide_index=True, use_container_width=True)
    st.caption(f"Total de colunas: {len(jp.columns)}")
else:
    st.error("❌ Arquivo 'Job Profile.xlsx' não foi encontrado.")

st.divider()

if "level_structure" in DATA:
    ls = DATA["level_structure"]
    st.subheader("🏗️ Level Structure.xlsx — Colunas encontradas")
    st.dataframe(pd.DataFrame({"Column": ls.columns}), hide_index=True, use_container_width=True)
    st.caption(f"Total de colunas: {len(ls.columns)}")
else:
    st.warning("⚠️ Arquivo 'Level Structure.xlsx' não encontrado ou sem colunas legíveis.")
