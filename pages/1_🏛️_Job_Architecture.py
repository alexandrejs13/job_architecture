import streamlit as st
from utils.data_loader import load_excel_data

st.set_page_config(layout="wide", page_title="🏛️ Job Architecture")

data = load_excel_data()
if "job_family" not in data:
    st.error("⚠️ Arquivo 'Job Family.xlsx' não encontrado.")
    st.stop()

df = data["job_family"]

st.markdown("## 🏛️ Job Architecture Overview")
st.markdown("""
Explore a estrutura corporativa de cargos, famílias e subfamílias.
Use este painel para visualizar a hierarquia global e entender como os papéis se relacionam.
""")

st.dataframe(df, use_container_width=True)
