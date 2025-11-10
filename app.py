import streamlit as st
from utils.ui import setup_sidebar, section

st.set_page_config(page_title="Recuperado", layout="wide")
setup_sidebar()
section("🏠 Home Recuperada")
st.write("O app voltou a funcionar!")
