import streamlit as st

# ===========================================================
# SIDEBAR: Logo + Título Centralizados e Alinhados com o Conteúdo
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

        /* === Estrutura geral === */
        [data-testid="stSidebarNav"] {{
            margin-top: 165px !important; /* ajusta espaçamento para caber header fixo */
            border-top: none !important;
            border-bottom: none !important;
        }}

        /* === Header fixo centralizado e alinhado === */
        .sidebar-header {{
            position: fixed;
            top: 0;
            left: 0;
            width: 300px;
            height: 160px;
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
            width: 95px;  /* logo ajustado */
            margin-bottom: 6px; /* espaço menor entre logo e título */
        }}

        .sidebar-header h2 {{
            color: #000000;
            font-size: 1.3rem; /* equilibrado */
            font-weight: 800;
            margin: 0;
            line-height: 1.1;
        }}

        /* === Alinhamento visual com container azul === */
        [data-testid="stSidebar"] > div:first-child {{
            border-bottom: none !important;
            padding-left: 6px !important; /* ligeiro ajuste horizontal */
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
