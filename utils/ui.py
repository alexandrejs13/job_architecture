import streamlit as st

def setup_sidebar():
    # URL direta da imagem (RAW)
    LOGO_URL = "https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/SIG_Logo_RGB_Blue.png"

    st.markdown(
        f"""
        <style>
            /* --- 1. ESCONDER ELEMENTOS INDESEJADOS --- */
            header {{visibility: hidden;}}
            footer {{visibility: hidden;}}
            #MainMenu {{visibility: hidden;}}
            .st-emotion-cache-h5rgjs {{visibility: hidden; height: 0;}} /* 'Made with Streamlit' */

            /* Esconde especificamente o item 'app' do menu.
               Geralmente é o primeiro <li> dentro da navegação. */
            [data-testid="stSidebarNav"] > ul:first-child > li:first-child {{
                display: none !important;
            }}

            /* --- 2. ESTILO BASE DA BARRA LATERAL --- */
            [data-testid="stSidebar"] {{
                background-color: white !important;
                border-right: 1px solid #e0e0e0;
            }}
            /* Remove padding padrão do topo para termos controle total */
            [data-testid="stSidebar"] .block-container {{
                padding-top: 0rem;
            }}

            /* --- 3. INJEÇÃO DO LOGO NO TOPO (CSS TRICK) --- */
            /* Isso cria um elemento virtual ANTES do menu de navegação */
            [data-testid="stSidebarNav"]::before {{
                content: "";
                display: block;
                margin: 20px auto 20px auto; /* Espaçamento acima e abaixo do logo */
                width: 120px;  /* Largura similar ao site SIG.biz */
                height: 60px;  /* Altura estimada para manter proporção */
                background-image: url('{LOGO_URL}');
                background-size: contain;
                background-repeat: no-repeat;
                background-position: center;
            }}

            /* Adiciona o Título "Job Architecture" logo abaixo do logo virtual */
            [data-testid="stSidebarNav"]::after {{
                 content: "Job Architecture";
                 display: block;
                 text-align: center;
                 font-weight: 900;
                 font-size: 1.4rem;
                 color: #145efc; /* Azul SIG */
                 margin-bottom: 20px; /* Espaço entre o título e o início do menu */
                 border-bottom: 2px solid #f0f2f6;
                 padding-bottom: 15px;
            }}

            /* --- 4. ESTILIZAÇÃO DO MENU --- */
            [data-testid="stSidebarNav"] {{
                padding-top: 20px; /* Garante espaço para o logo injetado acima */
            }}
             /* Links normais */
            [data-testid="stSidebarNav"] a, [data-testid="stSidebarNav"] span {{
                color: #333333 !important;
                font-weight: 500 !important;
            }}
            /* Hover */
            [data-testid="stSidebarNav"] a:hover {{
                background-color: #eef6fc !important;
                color: #145efc !important;
            }}
            /* Item Ativo */
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
