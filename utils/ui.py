import streamlit as st
import base64
import os

# ==============================================================================
# 1. CONFIGURAÇÕES
# ==============================================================================
FONT_REGULAR = "assets/fonts/PPSIGFlow-Regular.ttf"
FONT_SEMIBOLD = "assets/fonts/PPSIGFlow-SemiBold.ttf"
LOGO_URL = "https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/SIG_Logo_RGB_Blue.png"

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
            h1 {{ font-size: 2.4rem !important; }} /* Título Principal */
            h2 {{ font-size: 1.8rem !important; }} /* Subtítulos */
            h3 {{ font-size: 1.4rem !important; }} /* Títulos de Seção */
            p, li, span, div {{ color: #333333; }} /* Texto corrido cinza escuro para leitura */

            /* --- CARDS ESTILO SIG (Classe personalizada) --- */
            .sig-card {{
                background-color: #f2efeb; /* Cor Sand do site */
                padding: 30px;
                border-radius: 30px; /* Cantos BEM arredondados */
                margin-bottom: 25px;
            }}
            .sig-card h3, .sig-card h4 {{
                margin-top: 0 !important;
            }}

            /* --- LIMPEZA --- */
            header, footer, #MainMenu, .st-emotion-cache-h5rgjs {{ visibility: hidden; }}
            [data-testid="stSidebarNav"] > ul:first-child > li:first-child {{ display: none !important; }}

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
                color: #145efc; font-size: 1.5rem; font-weight: 900;
                padding-bottom: 40px; margin-bottom: 20px;
                border-bottom: 2px solid #f0f2f6;
            }}

            /* --- MENU DE NAVEGAÇÃO (ESTILO PÍLULA) --- */
            [data-testid="stSidebarNav"] > ul {{ padding: 0 15px; }} /* Espaço lateral para as pílulas não colarem na borda */
            [data-testid="stSidebarNav"] a {{
                color: #333333 !important;
                font-weight: 500 !important;
                border-radius: 50px !important; /* FORMA DE PÍLULA */
                padding: 8px 20px !important;   /* Mais preenchimento interno */
                margin-bottom: 5px;             /* Espaço entre os itens */
                transition: all 0.2s;
            }}
            [data-testid="stSidebarNav"] a:hover {{
                background-color: #f2efeb !important; /* Sand claro no hover */
                color: #000000 !important;
            }}
            /* ITEM ATIVO (Pílula Azul Vibrante) */
            [data-testid="stSidebarNav"] a[aria-current="page"] {{
                background-color: #145efc !important; /* Azul SIG */
                color: white !important;
                font-weight: 700 !important;
                box-shadow: 0 4px 12px rgba(20, 94, 252, 0.25); /* Sombra suave azul */
            }}
            [data-testid="stSidebarNav"] a[aria-current="page"] span {{ color: white !important; }}
        </style>
        """,
        unsafe_allow_html=True
    )
