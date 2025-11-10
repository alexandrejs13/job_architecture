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
# 3. SETUP UI (CSS REFORÇADO)
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
            {font_css}
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
                color: {TEXT_GRAY} !important;
                font-weight: 500 !important;
                border-radius: 999px !important; /* Pílula */
                padding: 10px 24px !important;
                margin-bottom: 5px !important;
                transition: none !important;
                border: none !important;
                text-decoration: none !important;
            }}

            /* Remove emojis */
            [data-testid="stSidebarNav"] li a span:first-child {{ display: none !important; }}
            [data-testid="stSidebarNav"] li a span:last-child {{ display: inline-block !important; }}

            /* Hover (SÓ TEXTO AZUL) */
            [data-testid="stSidebarNav"] li a:hover {{
                background-color: transparent !important;
                color: {SIG_SKY} !important;
            }}
            [data-testid="stSidebarNav"] li a:hover span {{ color: {SIG_SKY} !important; }}

            /* --- ITEM ATIVO (PÍLULA AZUL FORÇADA) --- */
            /* Usa seletor mais específico para garantir precedência */
            ul[data-testid="stSidebarNavItems"] li a[aria-current="page"],
            [data-testid="stSidebarNav"] a[data-active="true"] {{
                background-color: {SIG_SKY} !important;
                color: #ffffff !important;
                font-weight: 700 !important;
                box-shadow: none !important;
            }}
            ul[data-testid="stSidebarNavItems"] li a[aria-current="page"] span,
            [data-testid="stSidebarNav"] a[data-active="true"] span {{
                color: #ffffff !important;
            }}

        </style>
        """,
        unsafe_allow_html=True
    )
