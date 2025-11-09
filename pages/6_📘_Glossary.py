import streamlit as st
from utils.load_csv import load_csv_safe

st.set_page_config(page_title="Job Library", layout="wide")

st.markdown("<h1>📚 Job Library</h1>", unsafe_allow_html=True)

try:
    df = load_csv_safe("Job Profile.csv")
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

families = sorted(df["Job Family"].dropna().unique()) if "Job Family" in df.columns else []
family = st.selectbox("Selecione a Family", ["—"] + families)

if family == "—":
    st.info("Escolha uma Family para visualizar os cargos.")
    st.stop()

filtered = df[df["Job Family"] == family]
st.dataframe(filtered)
