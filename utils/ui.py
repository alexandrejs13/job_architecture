import streamlit as st

# ===========================================================
# 1. SIDEBAR COM LOGO E TÍTULO FIXOS ACIMA DO MENU
# ===========================================================
def sidebar_logo_and_title():
    logo_url = "https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/SIG_Logo_RGB_Blue.png"

    st.sidebar.markdown(f"""
    <style>
        /* === Cabeçalho fixo dentro da sidebar === */
        [data-testid="stSidebar"] .sidebar-header {{
            position: sticky;
            top: 0;
            background-color: #ffffff;
            text-align: center;
            padding: 22px 10px 14px 10px;
            border-bottom: 1px solid rgba(0, 0, 0, 0.1);
            z-index: 999;
        }}

        [data-testid="stSidebar"] .sidebar-header img {{
            width: 110px;
            margin-bottom: 4px;
            opacity: 0.95;
        }}

        [data-testid="stSidebar"] .sidebar-header h2 {{
            color: #145efc;
            font-weight: 800;
            font-size: 1.35rem;
            margin: 0;
        }}

        /* === Ajuste do menu abaixo === */
        [data-testid="stSidebarNav"] {{
            margin-top: 10px !important;
        }}
    </style>

    <div class="sidebar-header">
        <img src="{logo_url}" alt="SIG Logo">
        <h2>Job Architecture</h2>
    </div>
    """, unsafe_allow_html=True)


# ===========================================================
# 2. HEADER AZUL NAS PÁGINAS
# ===========================================================
def header(title: str, icon_url: str | None = None):
    """
    Exibe um cabeçalho azul padronizado com ícone e título.
    Usa URL absoluta para carregar o ícone.
    """
    icon_html = f'<img src="{icon_url}" width="30" style="vertical-align:middle; margin-right:10px;">' if icon_url else ""

    st.markdown(f"""
    <div style="
        background-color: #2962ff;
        color: white;
        padding: 14px 20px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        margin-bottom: 24px;
    ">
        {icon_html}
        <span style="font-size:1.5rem; font-weight:800;">{title}</span>
    </div>
    """, unsafe_allow_html=True)
