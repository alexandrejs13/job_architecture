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
# 3. SETUP UI (SOLUÇÃO NUCLEAR)
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
            /* --- FONTES E LIMPEZA --- */
            {font_css}
            header, footer, #MainMenu, .st-emotion-cache-h5rgjs {{ visibility: hidden !important; }}

            /* Oculta o 'app' de forma agressiva */
            [data-testid="stSidebarNav"] > ul:first-child {{ margin-top: 0 !important; }}
            [data-testid="stSidebarNav"] div[data-testid="stSidebarNavItems"] + div {{ display: none !important; }}
            /* Tenta pegar o título 'app' por posição se ele for um elemento solto */
            [data-testid="stSidebarContent"] > div:first-child > div:first-child > div:first-child {{ display: none !important; }}

            /* --- SIDEBAR TRAVADA --- */
            [data-testid="stSidebar"] {{
                min-width: 300px !important; max-width: 300px !important; width: 300px !important;
                background-color: white !important; border-right: 1px solid #f0f0f0 !important;
            }}
            div[data-testid="stSidebar"] > div:last-child {{ display: none !important; }}

            /* --- CABEÇALHO CUSTOMIZADO --- */
            [data-testid="stSidebarNav"] {{
                background-image: url('{LOGO_URL}'); background-repeat: no-repeat;
                background-position: center 20px; background-size: 100px auto;
                padding-top: 180px !important; /* Espaço para logo e título */
            }}
            [data-testid="stSidebarNav"]::before {{
                content: "Job Architecture"; display: block; text-align: center;
                color: {TEXT_BLACK} !important; font-size: 1.5rem; font-weight: 900;
                margin-top: -50px; margin-bottom: 30px;
                border-bottom: 2px solid #f0f2f6; padding-bottom: 20px;
            }}

            /* --- MENU NUCLEAR --- */
            /* 1. Reseta TODOS os itens do menu para o estilo base (inativo) */
            [data-testid="stSidebarNav"] a, [data-testid="stSidebarNav"] li {{
                background-color: transparent !important;
                color: {TEXT_GRAY} !important;
                font-weight: 500 !important;
                border: none !important;
            }}
            /* Transforma os links em pílulas */
            [data-testid="stSidebarNav"] a {{
                border-radius: 999px !important;
                padding: 10px 24px !important;
                margin: 0px 10px 5px 10px !important; /* Margens laterais para não colar na borda */
            }}
            
            /* 2. Oculta Emojis */
            [data-testid="stSidebarNav"] a span:first-child {{ display: none !important; }}
            [data-testid="stSidebarNav"] a span:last-child {{ display: inline-block !important; }}

            /* 3. Hover (apenas texto azul) */
            [data-testid="stSidebarNav"] a:hover {{
                color: {SIG_SKY} !important;
            }}
            [data-testid="stSidebarNav"] a:hover span {{
                color: {SIG_SKY} !important;
            }}

            /* 4. ATIVO - FORÇA BRUTA PARA A PÍLULA AZUL */
            /* Seletor que busca qualquer link que tenha o atributo de página atual */
            a[aria-current="page"],
            a[data-active="true"] {{
                background-color: {SIG_SKY} !important;
                box-shadow: none !important;
            }}
            /* Força a cor do texto dentro da pílula ativa */
            a[aria-current="page"] span,
            a[data-active="true"] span {{
                color: white !important;
                font-weight: 900 !important;
            }}

        </style>
        """,
        unsafe_allow_html=True
    )
