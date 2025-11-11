import streamlit as st

def sidebar_logo_and_title():
    """Exibe logo SIG e título acima do menu lateral"""
    st.markdown(
        """
        <style>
            section[data-testid="stSidebar"] > div:first-child {
                position: relative;
            }
        </style>
        <div class="sidebar-logo">
            <img src="https://github.com/alexandrejs13/job_architecture/raw/main/assets/SIG_Logo_RGB_Blue.png" alt="SIG Logo">
            <h2>Job Architecture</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

def header(title: str, icon_path: str):
    """Cabeçalho azul padrão SIG com ícone"""
    st.markdown(f"""
    <div class="header-bar">
        <img src="{icon_path}" class="header-icon">
        <div class="header-title">{title}</div>
    </div>
    """, unsafe_allow_html=True)
