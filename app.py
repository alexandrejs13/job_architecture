import streamlit as st
from utils.data_loader import load_data

st.set_page_config(
    page_title="Job Architecture",
    layout="wide",
    page_icon="🏛️"
)

with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.sidebar.title("Job Architecture")
st.sidebar.info("Navegue pelas seções")

st.title("🏛️ Job Architecture")
st.write("""
Este aplicativo permite explorar a estrutura de cargos corporativos:
**Famílias, Subfamílias, Perfis, Mapas e Níveis** — com busca inteligente por atividades.
""")

st.info("Selecione uma página no menu lateral para começar.")

# Carregar dados para cache inicial
_ = load_data()
