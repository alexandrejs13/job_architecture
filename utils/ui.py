import streamlit as st

def setup_sidebar():
    # URL do logo
    LOGO_URL = "https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/SIG_Logo_RGB_Blue.png"

    st.markdown(
        f"""
        <style>
            /* --- 1. LIMPEZA GERAL --- */
            header {{visibility: hidden;}}
            footer {{visibility: hidden;}}
            .st-emotion-cache-h5rgjs {{display: none;}}
            #MainMenu {{visibility: hidden;}}
            /* Oculta o primeiro item do menu (geralmente 'app' ou página inicial duplicada) */
            [data-testid="stSidebarNav"] > ul:first-child > li:first-child {{
                display: none !important;
            }}

            /* --- 2. CONTAINER DO CABEÇALHO (LOGO + TÍTULO) --- */
            /* Usamos o ::before do container de navegação para criar toda a área do cabeçalho */
            [data-testid="stSidebarNav"]::before {{
                content: "Job Architecture"; /* Texto do Título */
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                /* Altura fixa para o cabeçalho. Ajuste se quiser maior/menor */
                height: 180px;
                /* Imagem de fundo (o Logo) */
                background-image: url('{LOGO_URL}');
                background-repeat: no-repeat;
                background-position: center 30px; /* Posiciona o logo 30px do topo do container */
                background-size: 120px auto; /* Tamanho do logo */
                /* Estilo do Texto */
                color: #145efc; /* Azul SIG */
                font-size: 1.5rem;
                font-weight: 900;
                padding-top: 100px; /* Empurra o texto para baixo do logo */
                margin-bottom: 20px; /* Espaço entre o cabeçalho e o menu */
                border-bottom: 2px solid #f0f2f6; /* Linha divisória */
            }}

            /* --- 3. ESTILO DA BARRA E MENU --- */
            [data-testid="stSidebar"] {{
                background-color: white !important;
                border-right: 1px solid #e0e0e0;
            }}
            /* Ajuste fino para o menu não colar na linha divisória */
            [data-testid="stSidebarNav"] > ul {{
                padding-top: 10px;
            }}
            /* Links do Menu - Estado Normal */
            [data-testid="stSidebarNav"] a {{
                color: #333333 !important;
                font-weight: 500 !important;
            }}
            /* Links do Menu - Hover */
            [data-testid="stSidebarNav"] a:hover {{
                background-color: #eef6fc !important;
                color: #145efc !important;
            }}
            /* Links do Menu - Ativo (Página Atual) */
            [data-testid="stSidebarNav"] a[aria-current="page"] {{
                background-color: #145efc !important;
                color: white !important;
                font-weight: 700 !important;
            }}
            /* Garante que o texto do item ativo fique branco */
            [data-testid="stSidebarNav"] a[aria-current="page"] span {{
                color: white !important;
            }}

        </style>
        """,
        unsafe_allow_html=True
    )
