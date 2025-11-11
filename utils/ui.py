import streamlit as st

# ===========================================================
# SIDEBAR LIMPA — Logo centralizado e sem linha inferior
# ===========================================================
def sidebar_logo_and_title():
    logo_url = "https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/SIG_Logo_RGB_Blue.png"

    st.sidebar.markdown("""
    <style>
        /* Remove TODAS as bordas, sombras e pseudo-elementos da sidebar */
        section[data-testid="stSidebar"],
        [data-testid="stSidebarNav"],
        [data-testid="stSidebarNav"]::before,
        [data-testid="stSidebarNav"]::after,
        section[data-testid="stSidebar"] div,
        section[data-testid="stSidebar"] > div:first-child,
        section[data-testid="stSidebar"] [data-testid="stSidebarContent"],
        section[data-testid="stSidebar"] [data-testid="stDecoration"],
        section[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] {
            border: none !important;
            border-top: none !important;
            border-bottom: none !important;
            box-shadow: none !important;
            outline: none !important;
            background: #ffffff !important;
        }

        /* Remoção de divisores internos (o problema principal!) */
        [data-testid="stSidebar"] hr,
        [data-testid="stSidebar"] div:has(hr),
        [data-testid="stSidebar"] div[role="separator"],
        [data-testid="stSidebar"]::after {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            border: none !important;
        }

        /* Impede o Streamlit de recriar o divisor por sombra */
        [data-testid="stSidebar"]::before {
            content: none !important;
            display: none !important;
        }

        /* Bloqueia redimensionamento e garante alinhamento */
        section[data-testid="stSidebar"] {
            resize: none !important;
            overflow: hidden !important;
            min-width: 300px !important;
            max-width: 300px !important;
        }

        /* Menu e espaçamento refinado */
        [data-testid="stSidebarNav"] {
            margin-top: 140px !important;
            padding-bottom: 0 !important;
        }

        /* Header fixo com o logo centralizado */
        .sidebar-header {
            position: fixed;
            top: 72px; /* Alinhado ao container azul */
            left: 0;
            width: 300px;
            height: 100px;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: #ffffff !important;
            z-index: 100;
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
