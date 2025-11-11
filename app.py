import streamlit as st
from pathlib import Path

# Aplica estilos SIG
base_path = Path(__file__).parent / "assets"

with open(base_path / "fonts.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

with open(base_path / "theme.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
