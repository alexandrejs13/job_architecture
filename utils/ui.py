import streamlit as st

# ===========================================================
# 1. SIDEBAR LIMPA — Logo centralizado e sem linha inferior
# ===========================================================
def sidebar_logo_and_title():
    """Renderiza o logotipo e limpa a sidebar padrão do Streamlit."""
    logo_url = "https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/SIG_Logo_RGB_Blue.png"

    st.sidebar.markdown("""
    <style>
        /* Remove TODAS as bordas, sombras e pseudo-elementos da sidebar */
        section[data-testid="stSidebar"],
        [data-testid="stSidebarNav"],
        [data-testid="stSidebarNav"]::before,
        [data-testid="stSidebarNav"]::after,
        section[data-testid="stSidebar"] div,
        section[data-testid="stSidebar"] > div:first-child,
        section[data-testid="stSidebar"] [data-testid="stSidebarContent"],
        section[data-testid="stSidebar"] [data-testid="stDecoration"],
        section[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] {
            border: none !important;
            border-top: none !important;
            border-bottom: none !important;
            box-shadow: none !important;
            outline: none !important;
            background: #ffffff !important;
        }

        /* Remove divisores internos */
        [data-testid="stSidebar"] hr,
        [data-testid="stSidebar"] div:has(hr),
        [data-testid="stSidebar"] div[role="separator"],
        [data-testid="stSidebar"]::after {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            border: none !important;
        }

        /* Impede que o Streamlit recrie sombra divisória */
        [data-testid="stSidebar"]::before {
            content: none !important;
            display: none !important;
        }

        /* Bloqueia redimensionamento e garante alinhamento */
        section[data-testid="stSidebar"] {
            resize: none !important;
            overflow: hidden !important;
            min-width: 300px !important;
            max-width: 300px !important;
        }

        /* Menu e espaçamento refinado */
        [data-testid="stSidebarNav"] {
            margin-top: 140px !important;
            padding-bottom: 0 !important;
        }

        /* Header fixo com o logo centralizado */
        .sidebar-header {
            position: fixed;
            top: 72px; /* Alinhado ao container azul */
            left: 0;
            width: 300px;
            height: 100px;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: #ffffff !important;
            z-index: 100;
        }

        .sidebar-header img {
            width: 105px;
            height: auto;
            display: block;
        }
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.markdown(
        f'<div class="sidebar-header"><img src="{logo_url}" alt="SIG Logo"></div>',
        unsafe_allow_html=True
    )

# ===========================================================
# 2. CONFIGURAÇÃO PADRÃO — Mantém compatibilidade
# ===========================================================
def setup_sidebar():
    """Atalho que apenas chama a sidebar padrão com logotipo e estilo unificado."""
    sidebar_logo_and_title()

# ===========================================================
# 3. SEÇÃO DE CABEÇALHO (AZUL PADRÃO)
# ===========================================================
def section(title: str, icon_url: str = None):
    """
    Cria o cabeçalho azul padronizado no topo das páginas.
    :param title: Título da seção
    :param icon_url: URL do ícone (padrão: governance)
    """
    icon = icon_url or "https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/governance.png"
    st.markdown(f"""
    <div style='background-color:#145efc;
                color:white;
                font-weight:750;
                font-size:1.35rem;
                border-radius:12px;
                padding:22px 36px;
                display:flex;
                align-items:center;
                gap:18px;
                width:100%;
                box-sizing:border-box;
                margin-bottom:40px;
                box-shadow:0 4px 12px rgba(0, 0, 0, 0.15);'>
        <img src="{icon}" width="48" height="48" style="flex-shrink:0;">
        {title}
    </div>
    """, unsafe_allow_html=True)
