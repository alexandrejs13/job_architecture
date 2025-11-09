import streamlit as st
from utils.load_csv import load_csv_safe

st.set_page_config(page_title="Structure Level", layout="wide")

st.markdown("<h1>🏗️ Structure Level</h1>", unsafe_allow_html=True)

try:
    df = load_csv_safe("Level Structure.csv")
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

if df.empty:
    st.warning("Nenhum dado disponível.")
else:
    st.dataframe(df)
