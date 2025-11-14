# -*- coding: utf-8 -*-
import streamlit as st
from pathlib import Path

# ============================
# CONFIGURAÇÃO GLOBAL
# ============================
st.set_page_config(
    page_title="Job Architecture",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================
# CARREGAR CSS GLOBAL
# ============================
assets_path = Path(__file__).parent / "assets"
css_files = ["fonts.css", "theme.css", "menu.css"]

for css in css_files:
    css_path = assets_path / css
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ============================
# HOME SIMPLES
# (O Streamlit multipage cuida do menu lateral sozinho)
# ============================
st.title("🏛️ Job Architecture SIG")
st.write("Use o menu lateral para navegar entre as páginas.")
