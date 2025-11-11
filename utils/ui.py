import streamlit as st

def sidebar_logo_and_title():
    """Logo e título padrão na barra lateral"""
    st.sidebar.markdown(
        f"""
        <div style='text-align:center; padding:1rem 0 0.5rem 0;'>
            <img src="https://github.com/alexandrejs13/job_architecture/raw/main/assets/SIG_Logo_RGB_Blue.png"
                 width="160" alt="SIG Logo">
            <h2 style="font-family:'PP SIG Flow','Helvetica Neue',Arial,sans-serif;
                       color:#145EFC; margin-top:0.5rem; font-weight:600;">
                Job Architecture
            </h2>
        </div>
        <hr style='margin-top:0.5rem; margin-bottom:1.5rem; border:1px solid #f2efeb;'>
        """,
        unsafe_allow_html=True
    )

def header(title: str, icon_path: str):
    """Cabeçalho azul SIG com título e ícone"""
    st.markdown(f"""
    <div class="header-bar">
        <img src="{icon_path}" class="header-icon">
        <div class="header-title">{title}</div>
    </div>
    """, unsafe_allow_html=True)
