import streamlit as st
from utils.data_loader import load_level_structure_df

st.set_page_config(layout="wide", page_title="🏗️ Structure Level")

st.markdown("""
<style>
.block-container { max-width: 1400px !important; }
h1 { color:#1E56E0; font-weight:800; font-size:1.8rem; margin-bottom:1rem; }
</style>
""", unsafe_allow_html=True)

try:
    df = load_level_structure_df()
except Exception as e:
    st.error(f"Erro ao carregar Level Structure.xlsx: {e}")
else:
    st.markdown("<h1>🏗️ Level Structure</h1>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)
    st.caption(f"Linhas: {len(df)} • Colunas: {len(df.columns)}")
