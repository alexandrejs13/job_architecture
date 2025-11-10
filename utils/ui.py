import streamlit as st
import base64
import os

# ==============================================================================
# 1. CONFIGURAÇÕES
# ==============================================================================
FONT_REGULAR = "assets/fonts/PPSIGFlow-Regular.ttf"
FONT_SEMIBOLD = "assets/fonts/PPSIGFlow-SemiBold.ttf"
LOGO_URL = "https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/SIG_Logo_RGB_Blue.png"
SIG_SKY = "#145efc"
TEXT_BLACK = "#000000"
TEXT_GRAY = "#333333"

# ==============================================================================
# 2. AUXILIARES
# ==============================================================================
def get_font_base64(file_path):
    if not os.path.exists(file_path): return None
    with open(file_path, "rb") as f: data = f.read()
    return base64.b64encode(data).decode("utf-8")

# ==============================================================================
# 3. SETUP UI (VERSÃO 100% ESTÁVEL - SEM FLASH)
# ==============================================================================
def setup_sidebar():
    
    # --- 1. CABEÇALHO NATIVO (ZERO FLASH) ---
    # Isso usa a função oficial do Streamlit. É estável.
    # Ele coloca o logo no topo, antes do menu.
    st.logo(LOGO_URL)

    # --- 2. FONTES ---
    font_reg_b64 = get_font_base64(FONT_REGULAR)
    font_sb_b64 = get_font_base64(FONT_SEMIBOLD)
    font_css = ""
    if font_reg_b64 and font_sb_b64:
        font_css = f"""
        @font-face {{ font-family: 'PP SIG Flow'; src: url(data:font/ttf;base64,{font_reg_b64}) format('truetype'); font-weight: 400; font-style: normal; }}
        @font-face {{ font-family: 'PP SIG Flow'; src: url(data:font/ttf;base64,{font_sb_b64}) format('truetype'); font-weight: 700; font-style: normal; }}
        html, body, [class*="css"] {{ font-family: 'PP SIG Flow', sans-serif !important; }}
        """

    # --- 3. CSS MÍNIMO E ESTÁVEL ---
    # Apenas esconde elementos e ajusta fontes, sem mudar o layout (para não piscar)
    st.markdown(
        f"""
        <style>
            {font_css}

            /* --- TIPOGRAFIA --- */
            h1, h2, h3, h4, h5, h6 {{ color: {TEXT_BLACK} !important; font-weight: 700 !important; }}
            
            /* --- LIMPEZA --- */
            header, footer, #MainMenu, .st-emotion-cache-h5rgjs {{ display: none !important; }}
            
            /* OCULTA O PRIMEIRO ITEM ('app') */
            [data-testid="stSidebarNav"] > ul:first-child > li:first-child {{ display: none !important; }}
            
            /* OCULTA EMOJIS */
            [data-testid="stSidebarNav"] a span:first-child {{ display: none !important; }}
            [data-testid="stSidebarNav"] a span:last-child {{ display: inline-block !important; }}

            /* --- TRAVA SIDEBAR --- */
            [data-testid="stSidebar"] {{
                min-width: 300px !important; max-width: 300px !important; width: 300px !important;
                background-color: white !important; border-right: 1px solid #f0f0f0;
            }}
            div[data-testid="stSidebar"] > div:last-child {{ display: none; }} /* Esconde alça */

            /* --- AJUSTE FINO DO LOGO NATIVO --- */
            [data-testid="stSidebarLogo"] {{
                padding: 2.5rem 0; /* Centraliza verticalmente o logo */
                width: 100%;
                border-bottom: 2px solid #f0f2f6;
            }}
            [data-testid="stSidebarLogo"] img {{
                width: 100px; /* Tamanho elegante */
                margin: 0 auto;
            }}

            /* --- MENU NATIVO (Hover sutil) --- */
            [data-testid="stSidebarNav"] a:hover span {{
                color: {SIG_SKY} !important;
            }}
            
            /* Remove o padding excessivo que o menu nativo tem */
            [data-testid="stSidebarNav"] {{
                padding-top: 1rem !important;
            }}

        </style>
        """,
        unsafe_allow_html=True
    )
