import streamlit as st
import base64
import os

# ==============================================================================
# 1. CONFIGURAÇÕES
# ==============================================================================
FONT_REGULAR = "assets/fonts/PPSIGFlow-Regular.ttf"
FONT_SEMIBOLD = "assets.fonts/PPSIGFlow-SemiBold.ttf"
LOGO_URL = "https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/SIG_Logo_RGB_Blue.png"

# --- CORES DA PALETA SIG ---
SIG_SKY = "#145efc"    # Azul Principal
SIG_SAND = "#f2efeb"   # Bege Claro para Cards
TEXT_BLACK = "#000000" # Preto Puro para Títulos
TEXT_GRAY = "#333333"  # Cinza Escuro para Texto Corrido

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

            /* --- TIPOGRAFIA GLOBAL (Igual ao site SIG) --- */
            h1, h2, h3, h4, h5, h6 {{
                color: #000000 !important; /* Títulos PRETOS */
                font-weight: 700 !important; /* Sempre negrito (usa SemiBold) */
            }}
            h1 {{ font-size: 2.4rem !important; }}
            h2 {{ font-size: 1.8rem !important; }}
            h3 {{ font-size: 1.4rem !important; }}
            p, li, span, div {{ color: #333333; }}

            /* --- CARDS ESTILO SIG (Classe personalizada) --- */
            .sig-card {{
                background-color: #f2efeb; /* Cor Sand do site */
                padding: 30px;
                border-radius: 30px;
                margin-bottom: 25px;
            }}
            .sig-card h3, .sig-card h4 {{
                margin-top: 0 !important;
            }}

            /* --- LIMPEZA --- */
            header, footer, #MainMenu, .st-emotion-cache-h5rgjs {{ visibility: hidden; }}
            [data-testid="stSidebarNav"] > ul:first-child > li:first-child {{ display: none !important; }}
            /* Remove Emojis */
            [data-testid="stSidebarNav"] a span:first-child {{ display: none !important; }}
            [data-testid="stSidebarNav"] a span:last-child {{ display: inline-block !important; }}

            /* --- SIDEBAR --- */
            [data-testid="stSidebar"] {{
                min-width: 300px !important; max-width: 300px !important; width: 300px !important;
                background-color: white !important;
                border-right: 1px solid #f0f0f0;
            }}
            div[data-testid="stSidebar"] > div:last-child {{ display: none; }}

            /* --- CABEÇALHO SIDEBAR --- */
            [data-testid="stSidebarNav"]::before {{
                content: "Job Architecture";
                display: flex; flex-direction: column; align-items: center; justify-content: flex-end;
                height: 180px;
                background-image: url('{LOGO_URL}'); background-repeat: no-repeat;
                background-position: center 10px; background-size: 100px auto;
                color: {TEXT_BLACK} !important; /* COR PRETA NO TÍTULO */
                font-size: 1.5rem; font-weight: 900;
                padding-bottom: 40px; margin-bottom: 20px;
                border-bottom: 2px solid #f0f2f6;
            }}

            /* --- MENU DE NAVEGAÇÃO (ESTILO PÍLULA) --- */
            [data-testid="stSidebarNav"] > ul {{ padding: 0 15px; }}
            [data-testid="stSidebarNav"] a {{
                color: #333333 !important;
                font-weight: 500 !important;
                border-radius: 50px !important;
                padding: 8px 20px !important;
                margin-bottom: 5px;
                transition: none !important; /* REMOVE TRANSIÇÃO PARA PARAR O 'TILT' */
                background-color: transparent !important; /* Garante fundo transparente */
                border: 1px solid transparent !important; /* Evita 'tilt' de borda */
            }}
            [data-testid="stSidebarNav"] a:hover {{
                background-color: transparent !important; /* Sem fundo no hover */
                color: {SIG_SKY} !important; /* Apenas texto azul no hover */
            }}
            [data-testid="stSidebarNav"] a:hover span {{
                color: {SIG_SKY} !important;
            }}

            /* --- ITEM ATIVO (A PÍLULA AZUL FORÇADA) --- */
            [data-testid="stSidebarNav"] a[aria-current="page"] {{
                background-color: {SIG_SKY} !important; /* FORÇA O AZUL SIG SKY */
                color: white !important;                 /* FORÇA O TEXTO BRANCO */
                font-weight: 700 !important;
                box-shadow: none !important; /* REMOVE SOMBRA PARA PARAR O 'TILT' */
            }}
            [data-testid="stSidebarNav"] a[aria-current="page"] span {{
                color: white !important; /* FORÇA O SPAN INTERNO A SER BRANCO */
            }}
        </style>
        """,
        unsafe_allow_html=True
    )
