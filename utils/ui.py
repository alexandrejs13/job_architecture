import streamlit as st

def setup_sidebar():
    # URL direta da imagem (RAW) para carregar corretamente
    LOGO_URL = "https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/SIG_Logo_RGB_Blue.png"

    st.markdown(
        f"""
        <style>
            /* Esconde elementos padrão indesejados */
            header {{visibility: hidden;}}
            footer {{visibility: hidden;}}
            .st-emotion-cache-h5rgjs {{visibility: hidden; height: 0;}} /* Esconde 'Made with Streamlit' */
            [data-testid="stSidebarNav"] h3 {{display: none !important;}} /* Esconde o título 'app' do menu */

            /* --- ESTILO DA BARRA LATERAL --- */
            [data-testid="stSidebar"] {{
                background-color: white !important;
                border-right: 1px solid #e0e0e0;
            }}

            /* --- CABEÇALHO CUSTOMIZADO (LOGO + TÍTULO) --- */
            .custom-sidebar-header {{
                display: flex;
                flex-direction: column;
                align-items: flex-start;
                padding: 20px 15px 10px 15px;
                background-color: white;
                position: sticky;
                top: 0;
                z-index: 100;
                border-bottom: 2px solid #f0f2f6;
                margin-bottom: 10px;
            }}
            .logo-container {{
                display: flex;
                align-items: center;
                margin-bottom: 10px;
            }}
            .logo-container img {{
                height: 80px !important; /* Altura dobrada conforme solicitado */
                width: auto !important;  /* Mantém a proporção correta */
                object-fit: contain;
            }}
            .app-title {{
                color: #145efc; /* Azul SIG Sky */
                font-size: 1.5rem;
                font-weight: 900;
                margin: 0 !important;
                line-height: 1.2;
            }}

            /* --- MENU DE NAVEGAÇÃO --- */
            [data-testid="stSidebarNav"] {{
                padding-top: 0px;
            }}
            [data-testid="stSidebarNav"] ul {{
                padding-top: 10px;
            }}
            /* Links normais */
            [data-testid="stSidebarNav"] a, [data-testid="stSidebarNav"] span {{
                color: #333333 !important;
                font-weight: 500 !important;
            }}
            /* Hover (passar o mouse) */
            [data-testid="stSidebarNav"] a:hover {{
                background-color: #eef6fc !important; /* Fundo azul bem clarinho */
                color: #145efc !important; /* Texto azul SIG */
            }}
            /* Item Ativo (página atual) - Tenta pegar várias classes possíveis do Streamlit */
            [data-testid="stSidebarNav"] a[aria-current="page"],
            [data-testid="stSidebarNav"] a[data-active="true"] {{
                background-color: #145efc !important;
                color: white !important;
                font-weight: 700 !important;
            }}
            /* Garante que o texto dentro do item ativo também fique branco */
            [data-testid="stSidebarNav"] a[aria-current="page"] span,
            [data-testid="stSidebarNav"] a[data-active="true"] span {{
                color: white !important;
            }}

        </style>
        """,
        unsafe_allow_html=True
    )

    # Injeta o cabeçalho customizado no topo da sidebar
    st.sidebar.markdown(
        f"""
        <div class="custom-sidebar-header">
            <div class="logo-container">
                <img src="{LOGO_URL}" alt="SIG Logo">
            </div>
            <div class="app-title">Job Architecture</div>
        </div>
        """,
        unsafe_allow_html=True
    )
