# utils/ui.py

import streamlit as st

def setup_sidebar():
    st.markdown(
        """
        <style>
            /* Esconde o cabeçalho e o footer padrão do Streamlit */
            header { visibility: hidden; }
            footer { visibility: hidden; }

            /* Estilo para a barra lateral customizada */
            [data-testid="stSidebar"] {
                background-color: white !important; /* Fundo branco */
            }

            /* Container para o logo e título no topo da sidebar */
            .sidebar-header {
                display: flex;
                align-items: center;
                padding: 15px 20px 10px 20px; /* Mais espaço abaixo do header */
                background-color: white;
                border-bottom: 1px solid #f0f2f6; /* Linha sutil para separar */
                margin-bottom: 20px;
                position: sticky; /* Fixa o cabeçalho ao rolar */
                top: 0;
                z-index: 100;
            }

            .sidebar-header img {
                max-height: 80px; /* DOBRO: Aumentado de 40px para 80px */
                max-width: 80px;  /* DOBRO: Aumentado de 40px para 80px */
                margin-right: 15px;
                object-fit: contain;
            }

            .sidebar-header h1 {
                color: #145efc; /* Azul SIG */
                font-size: 1.8rem; /* Tamanho da fonte do título */
                font-weight: 900;
                margin: 0; /* Remove margem padrão do h1 */
                padding: 0;
            }

            /* Ajustes gerais para os links do menu (páginas) */
            [data-testid="stSidebarNav"] li a {
                color: #333333; /* Cor do texto dos links */
                font-size: 1rem;
                padding: 10px 20px;
                margin-bottom: 5px;
                border-radius: 8px; /* Bordas arredondadas para os itens */
                transition: all 0.2s ease-in-out;
            }

            [data-testid="stSidebarNav"] li a:hover {
                background-color: #f0f2f6; /* Fundo mais claro ao passar o mouse */
                color: #145efc; /* Cor do texto azul SIG ao passar o mouse */
                transform: translateX(5px); /* Efeito de deslizar leve */
            }

            /* Estilo para o link da página ativa */
            [data-testid="stSidebarNav"] li a.st-emotion-cache-1hdj7o2:focus, /* Para quando está ativo */
            [data-testid="stSidebarNav"] li a.st-emotion-cache-1hdj7o2[aria-current="page"] { /* Para quando está na página */
                background-color: #145efc !important; /* Fundo azul SIG */
                color: white !important; /* Texto branco */
                font-weight: 600;
                box-shadow: 0 4px 8px rgba(20, 94, 252, 0.2); /* Sombra sutil */
            }

            /* Esconde o "Made with Streamlit" */
            .st-emotion-cache-h5rgjs {
                visibility: hidden;
            }

            /* Ajusta margens para o conteúdo principal */
            .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Adiciona o logo e o título no topo da barra lateral
    st.sidebar.markdown(
        """
        <div class="sidebar-header">
            <img src="https://i.imgur.com/kF24v7b.png" alt="Logo SIG">
            <h1>JP Navigator</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Adiciona um espaço para empurrar os itens do menu para baixo do header customizado
    st.sidebar.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
