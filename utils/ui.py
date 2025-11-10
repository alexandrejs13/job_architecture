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
            .st-emotion-cache-h5rgjs {{display: none;}} /* 'Made with Streamlit' */
            #MainMenu {{visibility: hidden;}}

            /* Esconde o maldito item 'app' do menu */
            [data-testid="stSidebarNav"] > ul:first-child > li:first-child {{
                display: none !important;
            }}

            /* --- 2. INJEÇÃO DO CABEÇALHO VIA CSS --- */
            /* Alvo: o container de navegação da sidebar */
            [data-testid="stSidebarNav"] {{
                background-image: url('{LOGO_URL}');
                background-repeat: no-repeat;
                background-position: center 20px; /* 20px do topo */
                background-size: 120px auto; /* Largura do logo */
                padding-top: 120px !important; /* Espaço para o logo + texto */
            }}

            /* Injeta o texto "Job Architecture" DEPOIS do logo (via background) mas ANTES do menu */
            [data-testid="stSidebarNav"]::before {{
                content: "Job Architecture";
                display: block;
                text-align: center;
                font-weight: 900;
                font-size: 1.5rem;
                color: #145efc; /* Azul SIG */
                margin-top: -30px; /* Puxa pra cima, perto do logo */
                margin-bottom: 20px; /* Espaço até o primeiro item do menu */
                border-bottom: 2px solid #f0f2f6;
                padding-bottom: 15px;
            }}

            /* --- 3. ESTILO DA BARRA E MENU --- */
            [data-testid="stSidebar"] {{
                background-color: white !important;
                border-right: 1px solid #e0e0e0;
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
            /* Item Ativo */
            [data-testid="stSidebarNav"] a[aria-current="page"] {{
                background-color: #145efc !important;
                color: white !important;
            }}
            [data-testid="stSidebarNav"] a[aria-current="page"] span {{
                color: white !important;
            }}

        </style>
        """,
        unsafe_allow_html=True
    )
