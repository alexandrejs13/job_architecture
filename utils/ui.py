import streamlit as st

# ===========================================================
# SIDEBAR: Logo + Título Centralizados (sem borda ou sombra)
# ===========================================================
def sidebar_logo_and_title():
    logo_url = "https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/SIG_Logo_RGB_Blue.png"

    st.sidebar.markdown(f"""
    <style>
        /* === Estrutura geral do menu lateral === */
        [data-testid="stSidebarNav"] {{
            margin-top: 140px !important; /* espaço pro logo fixo */
            border-top: none !important;
            padding-top: 1rem !important;
        }}

        /* === Header fixo centralizado na sidebar === */
        .sidebar-header {{
            position: fixed;
            top: 0;
            left: 0;
            width: 300px; /* largura padrão da sidebar */
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            background-color: transparent; /* sem fundo */
            padding: 25px 10px 10px 10px;
            z-index: 100;
            box-shadow: none !important; /* remove sombra */
            border: none !important; /* remove borda */
        }}

        .sidebar-header img {{
            width: 115px;
            margin-bottom: 6px;
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
        icon_html = f'<img src="{icon_path}" alt="icon" style="width:26px;height:26px;margin-right:12px;vertical-align:middle;">'

    st.markdown(f"""
    <style>
        .page-header {{
            background-color: #145efc;
            color: white;
            font-weight: 700;
            font-size: 1.35rem; /* tamanho original */
            border-radius: 12px;
            padding: 12px 28px;
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 32px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
            width: fit-content;
        }}
    </style>

    <div class="page-header">
        {icon_html}
        {title}
    </div>
    """, unsafe_allow_html=True)
