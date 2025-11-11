import streamlit as st

# ===========================================================
# 1. LOGO E TÍTULO FIXOS NA SIDEBAR
# ===========================================================
def sidebar_logo_and_title():
    logo_url = "https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/SIG_Logo_RGB_Blue.png"

    st.sidebar.markdown(f"""
    <style>
        /* === Estrutura do menu lateral === */
        [data-testid="stSidebarNav"] {{
            margin-top: 180px !important; /* cria espaço pro header fixo */
            border-top: 2px solid rgba(0, 0, 0, 0.08);
            padding-top: 1rem !important;
        }}

        /* === Header fixo acima do menu === */
        .sidebar-header {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            text-align: center;
            background-color: #ffffff;
            padding-top: 28px;
            padding-bottom: 12px;
            z-index: 100;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        }}

        .sidebar-header img {{
            width: 120px;
            opacity: 0.95;
            margin-bottom: 6px;
        }}

        .sidebar-header h2 {{
            color: #145efc;
            font-size: 1.35rem;
            font-weight: 800;
            margin: 0;
        }}
    </style>

    <div class="sidebar-header">
        <img src="{logo_url}" alt="SIG Logo">
        <h2>Job Architecture</h2>
    </div>
    """, unsafe_allow_html=True)


# ===========================================================
# 2. CABEÇALHO DE PÁGINA (Título + Ícone)
# ===========================================================
def header(title: str, icon_path: str = None):
    """
    Exibe o cabeçalho superior de cada página (ícone + título).
    """
    icon_html = (
        f'<img src="{icon_path}" width="32" style="vertical-align:middle; margin-right:10px;">'
        if icon_path
        else ""
    )

    st.markdown(f"""
        <div style="display:flex; align-items:center; margin-bottom:0.8rem;">
            {icon_html}
            <h1 style="
                font-size:1.9rem;
                font-weight:800;
                color:#0d47a1;
                margin:0;
            ">{title}</h1>
        </div>
        <hr style="border:1px solid rgba(0,0,0,0.1); margin-top:0.4rem; margin-bottom:1.2rem;">
    """, unsafe_allow_html=True)
