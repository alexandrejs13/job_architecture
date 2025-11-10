# utils/ui.py
import streamlit as st

def setup_sidebar():
    # Caminho exato do seu arquivo de logo
    logo_path = "assets/SIG_Logo_RGB_White.png"

    # 1. Configura o Logo no topo da barra lateral
    # icon_image é usado quando a barra lateral está colapsada (opcional, mas recomendado)
    st.logo(logo_path, icon_image=logo_path)

    # 2. CSS para forçar o visual desejado: Fundo Preto (#000000) e Texto Branco (#ffffff)
    st.markdown(
        """
        <style>
            /* Define a cor de fundo da barra lateral para Preto SIG (#000000) */
            [data-testid="stSidebar"] {
                background-color: #000000;
            }
            /* Força TODOS os textos dentro da barra lateral para Branco (#ffffff) */
            [data-testid="stSidebar"] *, [data-testid="stSidebarNav"] span {
                color: #ffffff !important;
            }
            /* (Opcional) Ajuste de espaçamento para o menu não ficar colado no logo */
            [data-testid="stSidebarNav"] {
                padding-top: 1rem;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
