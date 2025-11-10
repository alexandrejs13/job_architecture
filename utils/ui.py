import streamlit as st
import base64
import os

# ==============================================================================
# 1. CONFIGURAÇÕES
# ==============================================================================
FONT_REGULAR = "assets/fonts/PPSIGFlow-Regular.ttf"
FONT_SEMIBOLD = "assets/fonts/PPSIGFlow-SemiBold.ttf"
LOGO_URL = "https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/SIG_Logo_RGB_Blue.png"

# CORES SIG
SIG_SKY = "#145efc"
TEXT_GRAY = "#333333"
TEXT_BLACK = "#000000"

# ==============================================================================
# 2. AUXILIARES
# ==============================================================================
def get_font_base64(file_path):
    if not os.path.exists(file_path): return None
    with open(file_path, "rb") as f: data = f.read()
    return base64.b64encode(data).decode("utf-8")

# ==============================================================================
# 3. SETUP UI (CSS GLOBAL)
# ==============================================================================
def setup_sidebar():
    font_reg_b64 = get_font_base64(FONT_REGULAR)
    font_sb_b64 = get_font_base64(FONT_SEMIBOLD)

    font_css = ""
    if font_reg_b64 and font_sb_b64:
        font_css = f"""
        @font-face {{ font-family: 'PP SIG Flow'; src: url(data:font/ttf;base64,{font_reg_b64}) format('truetype'); font-weight: 400; font-style: normal; }}
        @font-face {{ font-family: 'PP SIG Flow'; src: url(data:font/ttf;base64,{font_sb_b64}) format('truetype'); font-weight: 700; font-style: normal; }}
        html, body, [class*="css"] {{ font-family: 'PP SIG Flow', sans-serif !important; }}
        """

    st.markdown(
        f"""
        <style>
            /* --- FONTES --- */
            {font_css}

            /* --- TIPOGRAFIA GLOBAL --- */
            h1, h2, h3, h4, h5, h6 {{ color: {TEXT_BLACK} !important; font-weight: 700 !important; }}
            p, li, span, div {{ color: {TEXT_GRAY}; }}

            /* --- LIMPEZA --- */
            header, footer, #MainMenu, .st-emotion-cache-h5rgjs {{ visibility: hidden; }}
            [data-testid="stSidebarNav"] > ul:first-child > li:first-child {{ display: none !important; }}

            /* --- SIDEBAR TRAVADA --- */
            [data-testid="stSidebar"] {{
                min-width: 300px !important; max-width: 300px !important; width: 300px !important;
                background-color: white !important; border-right: 1px solid #f0f0f0;
            }}
            div[data-testid="stSidebar"] > div:last-child {{ display: none; }}

            /* --- CABEÇALHO --- */
            [data-testid="stSidebarNav"]::before {{
                content: "Job Architecture";
                display: flex; flex-direction: column; align-items: center; justify-content: flex-end;
                height: 180px;
                background-image: url('{LOGO_URL}'); background-repeat: no-repeat;
                background-position: center 10px; background-size: 100px auto;
                color: {SIG_SKY}; font-size: 1.5rem; font-weight: 900;
                padding-bottom: 40px; margin-bottom: 20px; border-bottom: 2px solid #f0f2f6;
            }}

            /* --- MENU DE NAVEGAÇÃO --- */
            [data-testid="stSidebarNav"] > ul {{ padding: 0 15px; }}
            
            /* Links Normais (Inativos) */
            [data-testid="stSidebarNav"] a {{
                color: {TEXT_GRAY} !important;
                font-weight: 500 !important;
                border-radius: 50px !important; /* Pílula sempre pronta */
                padding: 8px 20px !important;
                margin-bottom: 5px;
                transition: all 0.2s;
                background-color: transparent !important; /* Garante fundo transparente se não ativo */
            }}
            
            /* Hover (Passar o mouse) - APENAS MUDA COR DO TEXTO, SEM FUNDO */
            [data-testid="stSidebarNav"] a:hover {{
                color: {SIG_SKY} !important; /* Azul SIG Sky no texto ao passar o mouse */
                background-color: transparent !important; /* Sem pílula no hover */
            }}

            /* --- ITEM ATIVO (Página Atual) - AQUI A PÍLULA APARECE --- */
            [data-testid="stSidebarNav"] a[aria-current="page"] {{
                background-color: {SIG_SKY} !important; /* Fundo AZUL SIG SKY (#145efc) */
                color: white !important;                 /* Texto BRANCO (#ffffff) */
                font-weight: 700 !important;
                box-shadow: 0 4px 12px rgba(20, 94, 252, 0.25);
            }}
            /* Garante que o texto interno (span) fique branco também */
            [data-testid="stSidebarNav"] a[aria-current="page"] span {{
                color: white !important;
            }}

        </style>
        """,
        unsafe_allow_html=True
    )
