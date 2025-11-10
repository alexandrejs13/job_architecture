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
            /* Oculta o primeiro item do menu (geralmente 'app') */
            [data-testid="stSidebarNav"] > ul:first-child > li:first-child {{
                display: none !important;
            }}

            /* --- 2. TRAVAR BARRA LATERAL (IMPEDE REDIMENSIONAMENTO) --- */
            [data-testid="stSidebar"] {{
                min-width: 300px !important;
                max-width: 300px !important;
                width: 300px !important;
            }}
            /* Esconde a alça de redimensionamento */
            div[data-testid="stSidebar"] > div:last-child {{
                display: none;
            }}

            /* --- 3. CONTAINER DO CABEÇALHO (LOGO + TÍTULO) --- */
            [data-testid="stSidebarNav"]::before {{
                content: "Job Architecture";
                display: flex;
                flex-direction: column;
                align-items: center;
                /* 'flex-end' empurra o conteúdo para baixo, e o padding o traz de volta para cima */
                justify-content: flex-end;
                height: 180px; /* Altura total da área do cabeçalho */
                background-image: url('{LOGO_URL}');
                background-repeat: no-repeat;
                /* AJUSTE 1: Logo posicionado mais para cima (10px do topo) */
                background-position: center 10px;
                /* AJUSTE 2: Tamanho do logo um pouco menor (100px de largura) */
                background-size: 100px auto;
                color: #145efc; /* Azul SIG */
                font-size: 1.5rem;
                font-weight: 900;
                /* AJUSTE 3: Aumentei o padding-bottom para subir mais o bloco de texto/logo */
                padding-bottom: 40px;
                margin-bottom: 20px; /* Espaço entre a linha divisória e o menu */
                border-bottom: 2px solid #f0f2f6;
            }}

            /* --- 4. ESTILO DA BARRA E MENU --- */
            [data-testid="stSidebar"] {{
                background-color: white !important;
                border-right: 1px solid #e0e0e0;
            }}
            [data-testid="stSidebarNav"] > ul {{
                padding-top: 10px;
            }}
            /* Links do Menu */
            [data-testid="stSidebarNav"] a {{
                color: #333333 !important;
                font-weight: 500 !important;
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
