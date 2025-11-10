import streamlit as st
import base64, os

# ==============================================================================
# 1. CONFIGURAÇÕES
# ==============================================================================
FONT_REGULAR = "assets/fonts/PPSIGFlow-Regular.ttf"
FONT_SEMIBOLD = "assets/fonts/PPSIGFlow-SemiBold.ttf"
LOGO_URL = "https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/SIG_Logo_RGB_Blue.png"

# Paleta SIG
SIG_SKY = "#145efc"     # Azul principal
TEXT_BLACK = "#000000"
TEXT_GRAY = "#333333"

# ==============================================================================
# 2. AUXILIAR
# ==============================================================================
def get_font_base64(file_path):
    if not os.path.exists(file_path): return None
    with open(file_path, "rb") as f: return base64.b64encode(f.read()).decode("utf-8")

# ==============================================================================
# 3. CONFIGURAÇÃO DO LAYOUT E MENU
# ==============================================================================
def setup_sidebar():
    font_reg_b64 = get_font_base64(FONT_REGULAR)
    font_sb_b64 = get_font_base64(FONT_SEMIBOLD)
    font_css = ""
    if font_reg_b64 and font_sb_b64:
        font_css = f"""
        @font-face {{
            font-family: 'PP SIG Flow';
            src: url(data:font/ttf;base64,{font_reg_b64}) format('truetype');
            font-weight: 400; font-style: normal;
        }}
        @font-face {{
            font-family: 'PP SIG Flow';
            src: url(data:font/ttf;base64,{font_sb_b64}) format('truetype');
            font-weight: 700; font-style: normal;
        }}
        html, body, [class*="css"] {{
            font-family: 'PP SIG Flow', sans-serif !important;
        }}
        """

    st.markdown(
        f"""
        <style>
            {font_css}

            /* Remove header/footer nativos */
            header, footer, #MainMenu {{ display: none !important; }}
            [data-testid="stSidebarNav"] > ul:first-child > li:first-child {{ display: none !important; }}

            /* Sidebar fixa e estável */
            [data-testid="stSidebar"] {{
                min-width: 300px !important; max-width: 300px !important;
                background-color: white !important;
                border-right: 1px solid #eee;
                position: fixed !important;
            }}

            /* Cabeçalho SIG */
            [data-testid="stSidebar"]::before {{
                content: "";
                position: absolute; top: 20px; left: 0;
                width: 100%; height: 160px;
                background: url('{LOGO_URL}') no-repeat center 40px / 100px auto;
                border-bottom: 2px solid #f0f2f6;
                z-index: 10;
            }}

            /* Espaço do menu abaixo do cabeçalho */
            [data-testid="stSidebarNav"] {{
                padding-top: 190px !important;
                z-index: 9;
            }}

            /* Remove emojis */
            [data-testid="stSidebarNav"] a span:first-child {{ display: none !important; }}

            /* Estilo dos links */
            [data-testid="stSidebarNav"] a {{
                color: {TEXT_GRAY} !important;
                font-weight: 500 !important;
                padding: 10px 24px !important;
                margin: 6px 10px !important;
                border-radius: 30px !important;
                transition: all 0.2s ease-in-out !important;
                background-color: transparent !important;
                display: block !important;
                text-align: center;
            }}

            /* Hover (texto azul) */
            [data-testid="stSidebarNav"] a:hover span {{
                color: {SIG_SKY} !important;
            }}

            /* Item ativo — pílula azul */
            [data-testid="stSidebarNav"] a[aria-current="page"] {{
                background-color: {SIG_SKY} !important;
                color: white !important;
            }}
            [data-testid="stSidebarNav"] a[aria-current="page"] span {{
                color: white !important;
                font-weight: 700 !important;
            }}

            /* Ajuste de área principal (centralizada e tamanho fixo) */
            [data-testid="stAppViewContainer"] > div:first-child {{
                max-width: 1200px;
                margin: 0 auto !important;
                padding-top: 2rem !important;
            }}
            [data-testid="stAppViewContainer"] {{
                background-color: #ffffff !important;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ==============================================================================
# 4. EXEMPLO DE USO
# ==============================================================================
setup_sidebar()
st.title("Página de Exemplo")
st.write("O conteúdo da página fica centralizado, com largura máxima fixa e o menu lateral estável.")
