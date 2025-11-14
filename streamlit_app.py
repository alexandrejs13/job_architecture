# -*- coding: utf-8 -*-
import streamlit as st
from pathlib import Path

# ===========================================================
# CONFIGURAÇÃO GLOBAL DO STREAMLIT
# ===========================================================
st.set_page_config(
    page_title="Job Architecture",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================================================
# CARREGAR CSS GLOBAL (SIG)
# ===========================================================
assets_path = Path(__file__).parent / "assets"
css_files = ["fonts.css", "theme.css", "menu.css"]

for css in css_files:
    css_path = assets_path / css
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ===========================================================
# HOME / PÁGINA INICIAL (O STREAMLIT MULTIPAGE CARREGA O RESTO)
# ===========================================================
st.markdown("""
<h1 style="
    font-family:'PPSIGFlow';
    font-weight:600;
    font-size:26px;
    color:#000;
">
    🏛️ Job Architecture SIG
</h1>

<p style="
    font-family:'PPSIGFlow';
    font-size:16px;
    color:#333;
">
Bem-vindo ao sistema corporativo de Job Architecture.  
Use o menu lateral esquerdo para navegar entre as páginas.
</p>
""", unsafe_allow_html=True)
