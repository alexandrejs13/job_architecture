# utils/ui.py
import streamlit as st
from pathlib import Path

# =========================================================
# CARREGA O CSS GLOBAL DA PASTA /assets
# =========================================================

def apply_global_css():
    css_files = ["theme.css", "styles.css", "header.css"]
    for css in css_files:
        file_path = Path("assets") / css
        if file_path.exists():
            with open(file_path) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# =========================================================
# RENDERIZA O LOGO NO TOPO DA SIDEBAR (menu nativo continua)
# =========================================================

def sidebar_logo_and_title(logo_path):
    """
    Insere o logo SIG acima do menu nativo do Streamlit,
    mantendo tudo responsivo e 100% compatível com multipage.
    """
    apply_global_css()

    with st.sidebar:
        st.markdown(
            f"""
            <div style="
                width: 100%;
                text-align: center;
                padding-top: 12px;
                padding-bottom: 8px;
            ">
                <img src="{logo_path}" style="width: 150px;">
            </div>
            """,
            unsafe_allow_html=True
        )
