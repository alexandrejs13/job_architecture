import streamlit as st

# ===========================================================
# SIDEBAR: Logo + Título Centralizados (fixos, sem resize)
# ===========================================================
def sidebar_logo_and_title():
    logo_url = "https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/SIG_Logo_RGB_Blue.png"

    st.sidebar.markdown(f"""
    <style>
        /* === Bloqueia redimensionamento da sidebar === */
        section[data-testid="stSidebar"] {{
            resize: none !important;
            overflow: hidden !important;
            min-width: 300px !important;
            max-width: 300px !important;
        }}

        /* === Estrutura geral do menu lateral === */
        [data-testid="stSidebarNav"] {{
            margin-top: 200px !important; /* espaço abaixo do header fixo */
            border-top: none !important;
            padding-top: 1rem !important;
        }}

        /* === Header fixo centralizado === */
        .sidebar-header {{
            position: fixed;
            top: 0;
            left: 0;
            width: 300px;
            height: 180px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            background-color: #ffffff;
            z-index: 100;
            border: none !important;
            box-shadow: none !important;
        }}

        .sidebar-header img {{
            width: 120px;
            margin-bottom: 8px;
        }}

        .sidebar-header h2 {{
            color: #145efc;
            font-size: 1.2rem;
            font-weight: 800;
            margin: 0;
        }}

        /* Remove divisor inferior */
        [data-testid="stSidebarNav"]::after {{
            display: none !important;
        }}
    </style>

    <div class="sidebar-header">
        <img src="{logo_url}" alt="SIG Logo">
        <h2>Job Architecture</h2>
    </div>
    """, unsafe_allow_html=True)


# ===========================================================
# HEADER: Container Azul com Ícone e Título
# ===========================================================
def header(title, icon_path=None):
    icon_html = ""
    if icon_path:
        icon_html = f'<img src="{icon_path}" alt="icon" style="width:28px;height:28px;margin-right:12px;vertical-align:middle;">'

    st.markdown(f"""
    <style>
        .page-header {{
            background-color: #145efc;
            color: white;
            font-weight: 700;
            font-size: 1.4rem;
            border-radius: 12px;
            padding: 16px 36px;
            display: inline-flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 40px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }}
    </style>

    <div class="page-header">
        {icon_html}
        {title}
    </div>
    """, unsafe_allow_html=True)
