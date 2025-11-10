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
# 3. SETUP UI (VERSÃO ESTÁVEL & POSICIONADA)
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
            /* --- LIMPEZA --- */
            header, footer, #MainMenu, .st-emotion-cache-h5rgjs {{ display: none !important; }}
            [data-testid="stSidebarNav"] > ul:first-child > li:first-child {{ display: none !important; }}

            /* --- BARRA LATERAL --- */
            [data-testid="stSidebar"] {{
                min-width: 300px !important; max-width: 300px !important; width: 300px !important;
                background-color: white !important; border-right: 1px solid #f0f0f0;
            }}
            div[data-testid="stSidebar"] > div:last-child {{ display: none; }}

            /* --- CABEÇALHO FIXO (ESTÁVEL) --- */
            /* Usamos ::before no stSidebar para criar um cabeçalho que não depende do carregamento do menu */
            [data-testid="stSidebar"]::before {{
                content: "Job Architecture";
                position: absolute; top: 0; left: 0; width: 100%; height: 190px;
                background-color: white; z-index: 999; /* Fica por cima de qualquer flash de menu */
                border-bottom: 2px solid #f0f2f6;
                display: flex; flex-direction: column; align-items: center;
                /* LOGO: background-position controla a altura. Aumente 40px para descer mais. */
                background-image: url('{LOGO_URL}'); background-repeat: no-repeat;
                background-position: center 40px; background-size: 100px auto;
                /* TEXTO: padding-top empurra o texto para baixo do logo. Ajuste para aproximar/afastar. */
                padding-top: 125px;
                color: {TEXT_BLACK}; font-size: 1.5rem; font-weight: 900;
            }}

            /* --- MENU DE NAVEGAÇÃO --- */
            /* Empurra o menu para baixo para não ficar escondido atrás do cabeçalho fixo */
            [data-testid="stSidebarNav"] {{
                padding-top: 200px !important;
            }}
            [data-testid="stSidebarNav"] > ul {{ padding: 0 15px !important; }}

            /* ESTILO DOS LINKS (SEM EMOJI) */
            [data-testid="stSidebarNav"] a span:first-child {{ display: none !important; }}
            [data-testid="stSidebarNav"] a span:last-child {{ display: inline-block !important; }}
            
            [data-testid="stSidebarNav"] a {{
                color: {TEXT_GRAY} !important; font-weight: 500 !important;
                padding: 10px 24px !important; margin-bottom: 4px !important;
                background-color: transparent !important; transition: none !important;
            }}
            /* Hover Sutil */
            [data-testid="stSidebarNav"] a:hover span {{ color: {SIG_SKY} !important; }}

            /* ATIVO (MANTENDO O PADRÃO STREAMLIT POR ENQUANTO PARA EVITAR FLASH) */
             /* Se quiser tentar a pílula de novo, me avise, mas ela é a maior causadora de flash */
            [data-testid="stSidebarNav"] a[aria-current="page"] {{
                background-color: #f5f5f5 !important; /* Cinza bem claro nativo */
            }}
             [data-testid="stSidebarNav"] a[aria-current="page"] span {{
                color: {TEXT_BLACK} !important;
                font-weight: 900 !important;
            }}

        </style>
        """,
        unsafe_allow_html=True
    )
