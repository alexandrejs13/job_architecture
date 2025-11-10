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
# 3. SETUP UI (CSS DEFINITIVO)
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
            /* --- FONTES E LIMPEZA GERAL --- */
            {font_css}
            header, footer, #MainMenu, .st-emotion-cache-h5rgjs {{ visibility: hidden !important; height: 0px !important; }}
            
            /* Tenta esconder o menu nativo antes dele piscar */
            [data-testid="stSidebarNav"] > ul {{ opacity: 0; animation: fadeIn 0.2s ease-in-out forwards; }}
            @keyframes fadeIn {{ to {{ opacity: 1; }} }}

            /* --- REMOÇÃO DE EMOJIS (ICONES DO MENU) --- */
            /* O Streamlit coloca o emoji num span e o texto noutro. Escondemos o primeiro. */
            [data-testid="stSidebarNav"] a span:nth-child(1) {{
                display: none !important;
            }}
            /* Garante que o texto (segundo span) fique visível */
            [data-testid="stSidebarNav"] a span:nth-child(2) {{
                display: inline-block !important;
            }}

            /* --- TRAVAMENTO DA SIDEBAR --- */
            [data-testid="stSidebar"] {{
                min-width: 300px !important; max-width: 300px !important; width: 300px !important;
                background-color: white !important; border-right: 1px solid #f0f0f0 !important;
            }}
            [data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {{
                padding-top: 0rem !important;
            }}
            div[data-testid="stSidebar"] > div:last-child {{ display: none !important; }}

            /* --- CABEÇALHO CUSTOMIZADO --- */
            [data-testid="stSidebarNav"] {{
                background-image: url('{LOGO_URL}'); background-repeat: no-repeat;
                background-position: center 20px; background-size: 100px auto;
                padding-top: 180px !important;
            }}
            [data-testid="stSidebarNav"]::before {{
                content: "Job Architecture"; display: block; text-align: center;
                color: {TEXT_BLACK} !important; font-size: 1.5rem; font-weight: 900;
                margin-top: -50px; margin-bottom: 20px; padding-bottom: 20px;
                border-bottom: 2px solid #f0f2f6;
            }}

            /* --- ESTILIZAÇÃO DO MENU (PÍLULAS) --- */
            [data-testid="stSidebarNav"] > ul {{ padding: 0 15px !important; }}
            
            /* Esconde o primeiro item 'app' se existir */
            [data-testid="stSidebarNav"] > ul:first-child > li:first-child {{ display: none !important; }}

            /* Links Inativos (Base) */
            [data-testid="stSidebarNav"] a {{
                color: {TEXT_GRAY} !important;
                font-weight: 500 !important;
                border-radius: 999px !important; /* Pílula */
                padding: 10px 24px !important;
                margin-bottom: 4px !important;
                background-color: transparent !important;
                transition: none !important; /* Sem animação para reduzir pisca */
                border: none !important;
                text-decoration: none !important;
            }}

            /* Hover (Passar o mouse) */
            [data-testid="stSidebarNav"] a:hover {{
                color: {SIG_SKY} !important;
            }}
            [data-testid="stSidebarNav"] a:hover span {{
                color: {SIG_SKY} !important;
            }}

            /* --- ITEM ATIVO (PÍLULA AZUL) --- */
            /* Seletores reforçados para garantir aplicação */
            [data-testid="stSidebarNav"] a[aria-current="page"],
            [data-testid="stSidebarNav"] a[data-active="true"] {{
                background-color: {SIG_SKY} !important;
                box-shadow: none !important;
            }}
            [data-testid="stSidebarNav"] a[aria-current="page"] span,
            [data-testid="stSidebarNav"] a[data-active="true"] span {{
                color: #ffffff !important;
                font-weight: 700 !important;
            }}

        </style>
        """,
        unsafe_allow_html=True
    )
