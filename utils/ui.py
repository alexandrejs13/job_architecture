import streamlit as st
from pathlib import Path

# ===========================================================
# 1. INSERE O LOGO E TÍTULO NA BARRA LATERAL
# ===========================================================
def sidebar_logo_and_title():
    logo_path = "https://github.com/alexandrejs13/job_architecture/raw/main/assets/SIG_Logo_RGB_Blue.png"

    st.sidebar.markdown(f"""
    <style>
        /* Remove o item "app" do menu lateral */
        [data-testid="stSidebarNav"] ul li:first-child {{ display: none !important; }}

        /* Ajusta a barra lateral para comportar o logo */
        [data-testid="stSidebarNav"] {{
            padding-top: 150px !important;
        }}

        /* Contêiner do logo */
        .sidebar-header {{
            position: absolute;
            top: 20px;
            left: 0;
            width: 100%;
            text-align: center;
        }}

        .sidebar-header img {{
            width: 110px;
            opacity: 0.95;
            margin-bottom: 4px;
        }}

        .sidebar-header h2 {{
            color: #145efc;
            font-size: 1rem;
            font-weight: 700;
            margin: 0;
        }}
    </style>

    <div class="sidebar-header">
        <img src="{logo_path}" alt="SIG Logo">
        <h2>Job Architecture</h2>
    </div>
    """, unsafe_allow_html=True)

# ===========================================================
# 2. CABEÇALHO AZUL PADRÃO
# ===========================================================
def header(title: str, icon_path: str):
    """Cria o cabeçalho azul SIG com ícone lateral"""
    icon_full_path = Path(icon_path)
    if not icon_full_path.exists():
        icon_full_path = f"https://github.com/alexandrejs13/job_architecture/raw/main/{icon_path}"

    st.markdown(f"""
    <style>
        .header-bar {{
            display: flex;
            align-items: center;
            background-color: #145efc;
            padding: 0.8rem 1.2rem;
            border-radius: 12px;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        }}
        .header-bar img {{
            width: 28px;
            height: 28px;
            margin-right: 10px;
        }}
        .header-title {{
            font-size: 1.4rem;
            font-weight: 700;
        }}
    </style>
    <div class="header-bar">
        <img src="{icon_full_path}" alt="icon">
        <div class="header-title">{title}</div>
    </div>
    """, unsafe_allow_html=True)
