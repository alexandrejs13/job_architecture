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
# 3. SETUP UI (VERSÃO ESTÁVEL)
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
            /* --- FONTES E TIPOGRAFIA --- */
            {font_css}
            h1, h2, h3, h4, h5, h6 {{ color: {TEXT_BLACK} !important; font-weight: 700 !important; }}

            /* --- LIMPEZA DE ELEMENTOS NATIVOS --- */
            header {{ visibility: hidden; }}
            footer {{ visibility: hidden; }}
            #MainMenu {{ visibility: hidden; }}
            .st-emotion-cache-h5rgjs {{ display: none; }} /* 'Made with Streamlit' */

            /* OCULTA O PRIMEIRO ITEM DO MENU ('APP') - ESTÁVEL */
            [data-testid="stSidebarNav"] > ul:first-child > li:first-child {{
                display: none !important;
            }}

            /* --- BARRA LATERAL TRAVADA --- */
            [data-testid="stSidebar"] {{
                min-width: 300px !important;
                max-width: 300px !important;
                width: 300px !important;
                background-color: white !important;
                border-right: 1px solid #f0f0f0;
            }}
            /* Esconde alça de redimensionamento */
            div[data-testid="stSidebar"] > div:last-child {{ display: none; }}

            /* --- CABEÇALHO PERSONALIZADO (LOGO + TÍTULO) --- */
            [data-testid="stSidebarNav"] {{
                background-image: url('{LOGO_URL}');
                background-repeat: no-repeat;
                background-position: center 20px;
                background-size: 100px auto;
                padding-top: 180px !important; /* Espaço reservado para o cabeçalho */
            }}
            [data-testid="stSidebarNav"]::before {{
                content: "Job Architecture";
                display: block;
                text-align: center;
                color: {TEXT_BLACK} !important;
                font-size: 1.5rem;
                font-weight: 900;
                margin-top: -50px;
                margin-bottom: 20px;
                padding-bottom: 20px;
                border-bottom: 2px solid #f0f2f6;
            }}

            /* --- AJUSTES FINAIS NO MENU (SEM PÍLULAS) --- */
            /* Apenas esconde os emojis para ficar limpo */
            [data-testid="stSidebarNav"] a span:first-child {{
                display: none !important;
            }}
            [data-testid="stSidebarNav"] a span:last-child {{
                display: inline-block !important;
                color: {TEXT_GRAY};
                font-weight: 500;
            }}

            /* Pequeno ajuste de hover apenas na cor do texto (sutil e estável) */
            [data-testid="stSidebarNav"] a:hover span:last-child {{
                color: {SIG_SKY} !important;
            }}

        </style>
        """,
        unsafe_allow_html=True
    )
