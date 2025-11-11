import streamlit as st

# ===========================================================
# SIDEBAR: Apenas logo SIG centralizado e alinhado com o conteúdo principal
# ===========================================================
def sidebar_logo_and_title():
    logo_url = "https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/SIG_Logo_RGB_Blue.png"

    st.sidebar.markdown("""
    <style>
        /* === Bloqueia redimensionamento da sidebar === */
        section[data-testid="stSidebar"] {
            resize: none !important;
            overflow: hidden !important;
            min-width: 300px !important;
            max-width: 300px !important;
            border: none !important;
            box-shadow: none !important;
        }

        /* === Estrutura geral do menu === */
        [data-testid="stSidebarNav"] {
            margin-top: 140px !important;
            border-top: none !important;
            border-bottom: none !important;
            box-shadow: none !important;
        }

        /* Remove qualquer divisor abaixo do menu */
        [data-testid="stSidebarNav"]::after {
            display: none !important;
        }

        /* Remove divisores adicionais do container */
        section[data-testid="stSidebar"] > div:first-child {
            border-bottom: none !important;
            box-shadow: none !important;
        }

        /* === Header fixo com apenas o logo === */
        .sidebar-header {
            position: fixed;
            top: 72px; /* ajusta altura vertical para alinhar com o container azul */
            left: 0;
            width: 300px;
            height: 100px;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: #ffffff;
            z-index: 100;
            border: none !important;
            box-shadow: none !important;
        }

        .sidebar-header img {
            width: 105px;
            height: auto;
            display: block;
        }
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.markdown(
        f'<div class="sidebar-header"><img src="{logo_url}" alt="SIG Logo"></div>',
        unsafe_allow_html=True
    )
