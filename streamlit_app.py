# -*- coding: utf-8 -*-
import streamlit as st
from pathlib import Path

# CONFIGURAÇÃO GLOBAL
st.set_page_config(
    page_title="Job Architecture",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CARREGAR CSS
assets_path = Path(__file__).parent / "assets"

fonts_css = assets_path / "fonts.css"
theme_css = assets_path / "theme.css"

if fonts_css.exists():
    with open(fonts_css) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if theme_css.exists():
    with open(theme_css) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# PÁGINA INICIAL (HOMEPAGE)
st.title("🏛️ Job Architecture SIG")
st.write("Bem-vindo ao sistema de Job Architecture.")

st.info("Use o menu lateral para navegar entre as páginas.")
