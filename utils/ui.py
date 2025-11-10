import streamlit as st
import base64
import os

# ==============================================================================
# 1. CONFIGURAÇÕES (Caminhos exatos conforme seus links do GitHub)
# ==============================================================================
# Ajustei o nome do segundo arquivo para SemiBold
FONT_REGULAR = "assets/fonts/PPSIGFlow-Regular.ttf"
FONT_SEMIBOLD = "assets/fonts/PPSIGFlow-SemiBold.ttf"

LOGO_URL = "https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/SIG_Logo_RGB_Blue.png"

# ==============================================================================
# 2. FUNÇÕES AUXILIARES
# ==============================================================================
def get_font_base64(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode("utf-8")

# ==============================================================================
# 3. SETUP DA UI
# ==============================================================================
def setup_sidebar():
    # --- Carrega fontes locais e converte para Base64 ---
    font_reg_b64 = get_font_base64(FONT_REGULAR)
    font_sb_b64 = get_font_base64(FONT_SEMIBOLD)

    font_css = ""
    if font_reg_b64 and font_sb_b64:
        font_css = f"""
        /* Define a fonte Normal (Regular - peso 400) */
        @font-face {{
            font-family: 'PP SIG Flow';
            src: url(data:font/ttf;base64,{font_reg_b64}) format('truetype');
            font-weight: 400;
            font-style: normal;
        }}
        /* Define a fonte Negrito (usando o arquivo SemiBold para peso 700) */
        @font-face {{
            font-family: 'PP SIG Flow';
            src: url(data:font/ttf;base64,{font_sb_b64}) format('truetype');
            font-weight: 700;
            font-style: normal;
        }}
        /* Aplica globalmente */
        html, body, [class*="css"] {{
            font-family: 'PP SIG Flow', sans-serif !important;
        }}
        """

    st.markdown(
        f"""
        <style>
            /* INJEÇÃO DAS FONTES */
            {font_css}

            /* LIMPEZA GERAL */
            header {{visibility: hidden;}}
            footer {{visibility: hidden;}}
            #MainMenu {{visibility: hidden;}}
            .st-emotion-cache-h5rgjs {{display: none;}}
            [data-testid="stSidebarNav"] > ul:first-child > li:first-child {{ display: none !important; }}

            /* BARRA LATERAL TRAVADA */
            [data-testid="stSidebar"] {{
                min-width: 300px !important;
                max-width: 300px !important;
                width: 300px !important;
                background-color: white !important;
                border-right: 1px solid #e0e0e0;
            }}
            div[data-testid="stSidebar"] > div:last-child {{ display: none; }}

            /* CABEÇALHO (LOGO + TÍTULO) */
            [data-testid="stSidebarNav"]::before {{
                content: "Job Architecture";
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: flex-end;
                height: 180px;
                background-image: url('{LOGO_URL}');
                background-repeat: no-repeat;
                background-position: center 10px;
                background-size: 100px auto;
                color: #145efc;
                font-size: 1.5rem;
                font-weight: 900; /* Vai usar o arquivo SemiBold por causa do peso 700 */
                padding-bottom: 40px;
                margin-bottom: 20px;
                border-bottom: 2px solid #f0f2f6;
            }}

            /* MENU DE NAVEGAÇÃO */
            [data-testid="stSidebarNav"] > ul {{ padding-top: 10px; }}
            [data-testid="stSidebarNav"] a {{ color: #333333 !important; font-weight: 500 !important; }}
            [data-testid="stSidebarNav"] a:hover {{ background-color: #eef6fc !important; color: #145efc !important; }}
            [data-testid="stSidebarNav"] a[aria-current="page"] {{ background-color: #145efc !important; color: white !important; font-weight: 700 !important; }}
            [data-testid="stSidebarNav"] a[aria-current="page"] span {{ color: white !important; }}
        </style>
        """,
        unsafe_allow_html=True
    )
