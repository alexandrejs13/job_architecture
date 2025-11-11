import streamlit as st

def sidebar_logo_and_title():
    """Logo SIG e título centralizados acima do menu"""
    st.markdown(
        """
        <style>
            /* Garante que o container lateral aceite posição absoluta */
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
    """Cabeçalho azul SIG"""
    st.markdown(f"""
    <div class="header-bar">
        <img src="{icon_path}" class="header-icon">
        <div class="header-title">{title}</div>
    </div>
    """, unsafe_allow_html=True)
