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
# 3. SETUP UI (VERSÃO ANTI-FLASH)
# ==============================================================================
def setup_sidebar():
    # --- 1. INJEÇÃO NATIVA (Mais estável que CSS puro para layout) ---
    # Isso cria o cabeçalho fisicamente no DOM antes do menu
    with st.sidebar.container():
        st.markdown(
            f"""
            <div style="text-align: center; padding: 20px 0; margin-bottom: 20px; border-bottom: 2px solid #f0f2f6;">
                <img src="{LOGO_URL}" style="width: 100px; margin-bottom: 15px;">
                <div style="color: {TEXT_BLACK}; font-size: 1.5rem; font-weight: 900; font-family: 'PP SIG Flow', sans-serif;">
                    Job Architecture
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # --- 2. CARREGAMENTO DE FONTES ---
    font_reg_b64 = get_font_base64(FONT_REGULAR)
    font_sb_b64 = get_font_base64(FONT_SEMIBOLD)
    font_css = ""
    if font_reg_b64 and font_sb_b64:
        font_css = f"""
        @font-face {{ font-family: 'PP SIG Flow'; src: url(data:font/ttf;base64,{font_reg_b64}) format('truetype'); font-weight: 400; font-style: normal; }}
        @font-face {{ font-family: 'PP SIG Flow'; src: url(data:font/ttf;base64,{font_sb_b64}) format('truetype'); font-weight: 700; font-style: normal; }}
        html, body, [class*="css"] {{ font-family: 'PP SIG Flow', sans-serif !important; }}
        """

    # --- 3. CSS APENAS PARA ESTILO (Menos invasivo = menos flash) ---
    st.markdown(
        f"""
        <style>
            {font_css}
            /* Limpeza de elementos nativos */
            header {{ visibility: hidden; }}
            footer {{ visibility: hidden; }}
            #MainMenu {{ visibility: hidden; }}
            .st-emotion-cache-h5rgjs {{ display: none; }}

            /* Oculta o primeiro item 'app' */
            [data-testid="stSidebarNav"] > ul:first-child > li:first-child {{ display: none !important; }}

            /* Trava a Sidebar */
            [data-testid="stSidebar"] {{
                min-width: 300px !important; max-width: 300px !important; width: 300px !important;
                background-color: white !important; border-right: 1px solid #f0f0f0;
            }}
            div[data-testid="stSidebar"] > div:last-child {{ display: none; }}

            /* Ajuste fino do menu para não colar no nosso cabeçalho nativo */
            [data-testid="stSidebarNav"] {{
                padding-top: 0px !important; /* Removemos o padding gigante que causava o flash */
            }}

            /* Estilo simples dos links (sem pílulas para estabilidade) */
            [data-testid="stSidebarNav"] a {{
                color: {TEXT_GRAY} !important;
                font-weight: 500 !important;
            }}
            /* Hover sutil apenas na cor do texto */
            [data-testid="stSidebarNav"] a:hover span {{
                color: {SIG_SKY} !important;
            }}

            /* Remove emojis */
            [data-testid="stSidebarNav"] a span:first-child {{ display: none !important; }}
            [data-testid="stSidebarNav"] a span:last-child {{ display: inline-block !important; }}

        </style>
        """,
        unsafe_allow_html=True
    )
