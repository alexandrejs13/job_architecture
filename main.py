import streamlit as st

# Oculta header e barra lateral
st.set_page_config(page_title="Job Architecture", layout="wide", initial_sidebar_state="expanded")
st.markdown("<style>header {visibility: hidden;} footer {visibility: hidden;}</style>", unsafe_allow_html=True)

# Redireciona automaticamente para a primeira página
st.switch_page("pages/1_🏛️_Job_Architecture.py")
