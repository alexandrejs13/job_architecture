import streamlit as st

def setup_sidebar():
    """
    Configura o visual padrão da barra lateral:
    - Fundo Preto (#000000)
    - Logo SIG no topo
    - Textos do menu em Branco (#ffffff)
    """

    # 1. Definição do caminho do logo
    LOGO_PATH = "assets/SIG_Logo_RGB_White.png"

    # 2. Tenta usar o método nativo moderno (Streamlit 1.35+)
    # Isso coloca o logo fixo no topo, acima do menu de navegação.
    try:
        st.logo(LOGO_PATH, icon_image=LOGO_PATH)
    except AttributeError:
        # Fallback simples caso a versão do Streamlit seja antiga
        st.sidebar.image(LOGO_PATH, use_column_width=True)

    # 3. CSS Hack para forçar as cores exatas (Fundo Preto / Texto Branco)
    # O !important garante que este estilo vença qualquer padrão do Streamlit.
    st.markdown(
        """
        <style>
            /* Força o fundo da barra lateral para Preto Absoluto */
            [data-testid="stSidebar"] {
                background-color: #000000 !important;
            }
            /* Força TODOS os textos, ícones e links da barra lateral para Branco */
            [data-testid="stSidebar"] *,
            [data-testid="stSidebarNav"] span,
            [data-testid="stSidebarNav"] a,
            [data-testid="stSidebar"] p,
            [data-testid="stSidebar"] div {
                color: #ffffff !important;
            }
            /* Remove o sublinhado padrão dos links se houver */
            [data-testid="stSidebarNav"] a {
                text-decoration: none !important;
            }
             /* (Opcional) Aumenta um pouco o logo se ele estiver muito pequeno */
            [data-testid="stLogo"] {
                height: auto !important;
                max-width: 90% !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
