import streamlit as st
import os

def load_css(file_path):
    """Lê o arquivo CSS e o retorna como string."""
    if not os.path.exists(file_path):
        st.error(f"Arquivo CSS não encontrado em: {file_path}")
        return ""
    with open(file_path) as f:
        return f.read()

def setup_sidebar():
    """
    Carrega o CSS estático (anti-flash) e aplica fontes.
    """
    
    # Carrega o CSS do arquivo estático (MUITO mais rápido que st.markdown)
    css = load_css("assets/styles.css")
    
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
