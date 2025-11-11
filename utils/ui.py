import streamlit as st

# ===========================================================
# SIDEBAR LIMPA — Apenas logo SIG centralizado e sem divisor inferior
# ===========================================================
def sidebar_logo_and_title():
    logo_url = "https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/SIG_Logo_RGB_Blue.png"

    st.sidebar.markdown("""
    <style>
        /* === Remove qualquer linha, borda ou sombra da sidebar === */
        section[data-testid="stSidebar"],
        [data-testid="stSidebarNav"],
        [data-testid="stSidebarNav"]::after,
        [data-testid="stSidebarNav"]::before,
        section[data-testid="stSidebar"] > div:first-child,
        section[data-testid="stSidebar"] div[data-testid="stVerticalBlockBorderWrapper"],
        section[data-testid="stSidebar"] div[data-testid="stDecoration"],
        section[data-testid="stSidebar"] div[data-testid="stSidebarContent"] {
            border: none !important;
            box-shadow: none !important;
            outline: none !important;
            background: #fff !important;
        }

        /* Bloqueia redimensionamento da sidebar */
        section[data-testid="stSidebar"] {
            resize: none !important;
            overflow: hidden !important;
            min-width: 300px !important;
            max-width: 300px !important;
        }

        /* Reposiciona menu e remove espaços */
        [data-testid="stSidebarNav"] {
            margin-top: 140px !important;
            padding-bottom: 0 !important;
        }

        /* Header fixo com apenas o logo */
        .sidebar-header {
            position: fixed;
            top: 72px; /* alinhado ao container azul */
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
