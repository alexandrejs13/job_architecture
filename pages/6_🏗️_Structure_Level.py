import streamlit as st
import pandas as pd
from utils.data_loader import load_level_structure_df

st.set_page_config(page_title="🏗️ Structure Level", layout="wide")

st.markdown("""
<style>
h1 { color: #1E56E0; font-weight: 800; }
</style>
""", unsafe_allow_html=True)

st.markdown("## 🏗️ Structure Level")

df = load_level_structure_df()

st.dataframe(df, use_container_width=True)
st.caption(f"Total de colunas: {len(df.columns)}")
