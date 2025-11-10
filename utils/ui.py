import streamlit as st
import base64
import os

# ==============================================================================
# 1. CONFIGURAÇÕES GERAIS (Caminhos e URLs)
# ==============================================================================
# Caminhos locais para os arquivos de fonte
FONT_REGULAR = "assets/fonts/PPSIGFlow-Regular.ttf"
FONT_BOLD = "assets/fonts/PPSIGFlow-Bold.ttf"

# URL do logo para o cabeçalho da sidebar
LOGO_URL = "https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/SIG_Logo_RGB_Blue.png"

# ==============================================================================
# 2. FUNÇÕES AUXILIARES
# ==============================================================================
def get_font_base64(file_path):
    """Lê um arquivo e retorna seu conteúdo codificado em base64."""
    if not os.path.exists(file_path):
        # Em produção, pode ser útil logar isso ou usar st.warning
        # print(f"⚠️ Aviso: Fonte não encontrada em {file_path}")
        return None
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode("utf-8")

# ==============================================================================
# 3. FUNÇÃO PRINCIPAL DE CONFIGURAÇÃO DA UI
# ==============================================================================
def setup_sidebar():
    """
    Aplica a configuração global de UI:
    - Fontes customizadas (PP SIG Flow)
    - Barra lateral travada e estilizada
    - Cabeçalho customizado com Logo e Título
    - Ocultação de elementos padrão indesejados
    """
    
    # --- A. Carregamento das Fontes ---
    font_reg_b64 = get_font_base64(FONT_REGULAR)
    font_bold_b64 = get_font_base64(FONT_BOLD)

    font_face_css = ""
    # Só monta o CSS se ambas as fontes forem encontradas
    if font_reg_b64 and font_bold_b64:
        font_face_css = f"""
        @font-face {{
            font-family: 'PP SIG Flow';
            src: url(data:font/ttf;base64,{font_reg_b64}) format('truetype');
            font-weight: 400;
            font-style: normal;
        }}
        @font-face {{
            font-family: 'PP SIG Flow';
            src: url(data:font/ttf;base64,{font_bold_b64}) format('truetype');
            font-weight: 700;
            font-style: normal;
        }}
        /* Aplica a fonte a todo o app */
        html, body, [class*="css"] {{
            font-family: 'PP SIG Flow', sans-serif !important;
        }}
        /* Força títulos a usarem o peso Bold (700) */
        h1, h2, h3, h4, h5, h6, strong, b {{
            font-weight: 700 !important;
        }}
        """

    # --- B. Injeção do CSS Completo ---
    st.markdown(
        f"""
        <style>
            /* 1. Fontes Globais */
            {font_face_css}

            /* 2. Limpeza de Interface */
            header {{visibility: hidden;}}
            footer {{visibility: hidden;}}
            #MainMenu {{visibility: hidden;}}
            .st-emotion-cache-h5rgjs {{display: none;}} /* 'Made with Streamlit' */
            
            /* Oculta o primeiro item do menu ('app') */
            [data-testid="stSidebarNav"] > ul:first-child > li:first-child {{
                display: none !important;
            }}

            /* 3. Travamento da Barra Lateral */
            [data-testid="stSidebar"] {{
                min-width: 300px !important;
                max-width: 300px !important;
                width: 300px !important;
            }}
            /* Esconde a alça de redimensionamento */
            div[data-testid="stSidebar"] > div:last-child {{
                display: none;
            }}

            /* 4. Cabeçalho da Sidebar (Logo + Título) */
            [data-testid="stSidebarNav"]::before {{
                content: "Job Architecture";
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: flex-end; /* Alinha conteúdo na parte de baixo do bloco */
                height: 180px;
                background-image: url('{LOGO_URL}');
                background-repeat: no-repeat;
                background-position: center 10px; /* Logo 10px do topo */
                background-size: 100px auto; /* Logo com 100px de largura */
                color: #145efc; /* Azul SIG Sky */
                font-size: 1.5rem;
                font-weight: 900; /* Usa a fonte Bold */
                padding-bottom: 40px; /* Empurra o texto para cima */
                margin-bottom: 20px; /* Espaço até o menu */
                border-bottom: 2px solid #f0f2f6;
            }}

            /* 5. Estilização do Menu de Navegação */
            [data-testid="stSidebar"] {{
                background-color: white !important;
                border-right: 1px solid #e0e0e0;
            }}
            [data-testid="stSidebarNav"] > ul {{
                padding-top: 10px;
            }}
            [data-testid="stSidebarNav"] a {{
                color: #333333 !important;
                font-weight: 500 !important; /* Usa fonte Regular (ou médio se disponível) */
            }}
            [data-testid="stSidebarNav"] a:hover {{
                background-color: #eef6fc !important;
                color: #145efc !important;
            }}
            [data-testid="stSidebarNav"] a[aria-current="page"] {{
                background-color: #145efc !important;
                color: white !important;
                font-weight: 700 !important;
            }}
            [data-testid="stSidebarNav"] a[aria-current="page"] span {{
                color: white !important;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )
