# -*- coding: utf-8 -*-
import streamlit as st
from pathlib import Path
import sys

# ======================================================
# CONFIGURAÇÃO DA APLICAÇÃO (MAIN ENTRYPOINT)
# ======================================================
st.set_page_config(
    page_title="Job Architecture",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# GARANTIR QUE O PYTHON ENXERGUE O PACOTE job_architecture
# ======================================================
ROOT_DIR = Path(__file__).resolve().parent
sys.path.append(str(ROOT_DIR))

# ======================================================
# CARREGAR ESTILOS SIG
# ======================================================
assets_path = ROOT_DIR / "assets"

fonts_css = assets_path / "fonts.css"
theme_css = assets_path / "theme.css"

if fonts_css.exists():
    with open(fonts_css, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if theme_css.exists():
    with open(theme_css, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ======================================================
# HOME PAGE DO APP
# ======================================================
st.title("🏛️ Job Architecture")
st.write("""
Bem-vindo ao ambiente de Job Architecture SIG.  
Use o menu lateral para navegar entre:

- Job Families  
- Job Profile Description  
- Job Maps  
- Job Match (GGS)  
- Structure Levels  
- Dashboard  

Todos os módulos usam a identidade visual SIG e carregam dados da pasta `/data`.
""")

st.markdown("---")
st.success("A aplicação está carregada. Selecione um módulo na barra lateral.")
