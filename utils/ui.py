import streamlit as st
import os

# ==============================================================================
# 1. CONFIGURAÇÕES
# ==============================================================================
LOGO_URL = "https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/SIG_Logo_RGB_Blue.png"

# --- CORES DA PALETA SIG ---
SIG_SKY = "#145efc"    # Azul Principal (Pantone 2387 C)
TEXT_BLACK = "#000000" # Preto Puro para Títulos

# ==============================================================================
# 2. SETUP UI (CSS GLOBAL DEFINITIVO)
# ==============================================================================
def setup_sidebar():
    # A lógica de carregamento de fontes foi removida para simplificar e evitar SyntaxError.
    # Se precisar das fontes, você pode injetá-las em um st.markdown separado ou usar um arquivo .css.

    st.markdown(
        f"""
        <style>
            /* Oculta elementos nativos */
            header, footer, #MainMenu, .st-emotion-cache-h5rgjs {{ visibility: hidden !important; }}
            [data-testid="stSidebarNav"] > ul:first-child > li:first-child {{ display: none !important; }}

            /* Sidebar Travada */
            [data-testid="stSidebar"] {{
                min-width: 300px !important; max-width: 300px !important; width: 300px !important;
                background-color: white !important; border-right: 1px solid #f0f0f0 !important;
            }}
            div[data-testid="stSidebar"] > div:last-child {{ display: none !important; }}

            /* Cabeçalho */
            [data-testid="stSidebarNav"]::before {{
                content: "Job Architecture"; display: flex; flex-direction: column; align-items: center; justify-content: flex-end;
                height: 180px; background-image: url('{LOGO_URL}'); background-repeat: no-repeat; background-position: center 10px; background-size: 100px auto;
                color: {TEXT_BLACK} !important; font-size: 1.5rem; font-weight: 900; padding-bottom: 40px; margin-bottom: 20px; border-bottom: 2px solid #f0f2f6;
            }}

            /* --- MENU DE NAVEGAÇÃO --- */
            [data-testid="stSidebarNav"] > ul {{ padding: 0 15px !important; }}

            /* Reset dos Links */
            [data-testid="stSidebarNav"] li a {{
                background-color: transparent !important;
                color: {TEXT_BLACK} !important; /* Cor do texto padrão: Preto */
                font-weight: 500 !important;
                border-radius: 999px !important; /* Pílula */
                padding: 10px 24px !important;
                margin-bottom: 5px !important;
                transition: color 0.2s, background-color 0.2s !important;
                border: none !important;
                text-decoration: none !important;
            }}

            /* Remove emojis */
            [data-testid="stSidebarNav"] li a span:first-child {{ display: none !important; }}
            [data-testid="stSidebarNav"] li a span:last-child {{ display: inline-block !important; }}

            /* Hover (SÓ TEXTO AZUL) */
            [data-testid="stSidebarNav"] li a:hover {{
                background-color: transparent !important;
                color: {SIG_SKY} !important; /* Texto azul no hover */
            }}
            [data-testid="stSidebarNav"] li a:hover span {{ color: {SIG_SKY} !important; }}

            /* --- ITEM ATIVO (PÍLULA AZUL FORÇADA) --- */
            /* Usa seletor mais específico para garantir precedência */
            ul[data-testid="stSidebarNavItems"] li a[aria-current="page"],
            [data-testid="stSidebarNav"] a[data-active="true"] {{
                background-color: {SIG_SKY} !important; /* Pílula azul */
                color: #ffffff !important; /* Texto branco */
                font-weight: 700 !important;
                box-shadow: none !important;
            }}
            ul[data-testid="stSidebarNavItems"] li a[aria-current="page"] span,
            [data-testid="stSidebarNav"] a[data-active="true"] span {{
                color: #ffffff !important; /* Texto branco */
            }}

            /* Garante que o hover não afete o item ativo */
            ul[data-testid="stSidebarNavItems"] li a[aria-current="page"]:hover,
            [data-testid="stSidebarNav"] a[data-active="true"]:hover {{
                background-color: {SIG_SKY} !important; /* Mantém a pílula azul */
                color: #ffffff !important; /* Mantém o texto branco */
            }}
            ul[data-testid="stSidebarNavItems"] li a[aria-current="page"]:hover span,
            [data-testid="stSidebarNav"] a[data-active="true"]:hover span {{
                color: #ffffff !important; /* Mantém o texto branco */
            }}

        </style>
        """,
        unsafe_allow_html=True
    )


ao vivo
