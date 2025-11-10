import streamlit as st
from utils.ui import setup_sidebar, section

# 1. Configuração da Página (SEMPRE EM PRIMEIRO LUGAR)
st.set_page_config(
    page_title="Job Architecture",
    page_icon="🏠",
    layout="wide"
)

# 2. Aplica o CSS imediatamente
setup_sidebar()

# 3. Conteúdo da Página
section("🏠 Home")

st.write("Bem-vindo ao sistema de Job Architecture.")
