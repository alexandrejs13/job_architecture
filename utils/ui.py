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

            /* --- 2. POSICIONAMENTO DO LOGO (BACKGROUND) --- */
            [data-testid="stSidebarNav"] {{
                background-image: url('{LOGO_URL}');
                background-repeat: no-repeat;
                background-position: center 20px; /* Logo 20px do topo */
                background-size: 120px auto; /* Largura do logo */
                padding-top: 120px !important; /* Espaço reservado para logo + título */
            }}

            /* --- 3. POSICIONAMENTO DO TÍTULO (TEXTO) --- */
            [data-testid="stSidebarNav"]::before {{
                content: "Job Architecture";
                display: block;
                text-align: center;
                font-weight: 900;
                font-size: 1.5rem;
                color: #145efc; /* Azul SIG */
                margin-top: 0px; /* Ajuste fino da distância entre logo e texto */
                margin-bottom: 20px; /* Espaço entre o título e o primeiro item do menu */
                border-bottom: 2px solid #f0f2f6; /* Linha separadora */
                padding-bottom: 15px;
            }}

            /* --- 4. ESTILO DA BARRA E MENU --- */
            [data-testid="stSidebar"] {{
                background-color: white !important;
                border-right: 1px solid #e0e0e0;
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
