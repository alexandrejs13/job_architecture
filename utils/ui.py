import streamlit as st

# ===========================================================
# SIDEBAR: Apenas logo SIG centralizado e alinhado com o conteúdo principal
# ===========================================================
def sidebar_logo_and_title():
    logo_url = "https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/SIG_Logo_RGB_Blue.png"

    # usamos triple quotes normais sem f-string, e depois concatenamos manualmente o logo_url
    st.sidebar.markdown("""
    <style>
        /* === Bloqueia redimensionamento da sidebar === */
        section[data-testid="stSidebar"] {
            resize: none !important;
            overflow: hidden !important;
            min-width: 300px !important;
            max-width: 300px !important;
        }

        /* === Estrutura geral do menu === */
        [data-testid="stSidebarNav"] {
            margin-top: 140px !important; /* ajusta espaçamento para o logo */
            border-top: none !important;
            border-bottom: none !important;
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
            width: 105px;  /* logo maior, proporcional ao novo layout */
            height: auto;
            display: block;
        }

        /* Remove divisores padrão do Streamlit */
        [data-testid="stSidebarNav"]::after {
            display: none !important;
        }
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.markdown(
        f'<div class="sidebar-header"><img src="{logo_url}" alt="SIG Logo"></div>',
        unsafe_allow_html=True
    )
