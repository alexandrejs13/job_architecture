import streamlit as st

def setup_sidebar():
    """
    Configura a barra lateral: Fundo Branco, Logo Azul SIG.
    Ajusta o estilo do menu para ser limpo e profissional.
    """
    # Caminho do novo logo azul
    LOGO_PATH = "assets/SIG_Logo_RGB_Blue.png"

    # 1. Aplica o Logo (tenta método moderno, fallback para antigo)
    try:
        st.logo(LOGO_PATH, icon_image=LOGO_PATH)
    except AttributeError:
        st.sidebar.image(LOGO_PATH, use_column_width=False, width=180)

    # 2. CSS para Refinamento do Visual
    st.markdown(
        """
        <style>
            /* --- BARRA LATERAL --- */
            /* Garante fundo branco (redundância ao config.toml para segurança) */
            [data-testid="stSidebar"] {
                background-color: #ffffff !important;
                border-right: 1px solid #e0e0e0; /* Linha sutil separando o menu */
            }

            /* --- MENU DE NAVEGAÇÃO --- */
            /* Texto dos links do menu: Preto suave, sem sublinhado */
            [data-testid="stSidebarNav"] a,
            [data-testid="stSidebarNav"] span {
                color: #333333 !important;
                text-decoration: none !important;
                font-weight: 500;
            }
            /* Efeito Hover (quando passa o mouse): Fica azulzinho claro */
            [data-testid="stSidebarNav"] a:hover {
                background-color: #f0f5ff !important; /* Azul muito suave */
                color: #145efc !important; /* Azul SIG Sky no texto */
            }

            /* --- AJUSTES GERAIS --- */
            /* Título e textos na sidebar também escuros */
            [data-testid="stSidebar"] .stMarkdown,
            [data-testid="stSidebar"] p {
                 color: #333333 !important;
            }
            /* Oculta o item 'app' ou 'Home' do menu se ele for o primeiro e redundante */
            /* Remova as 3 linhas abaixo se quiser que o primeiro item apareça */
            ul[data-testid="stSidebarNavItems"] > li:first-child {
                display: none !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
