import streamlit as st

# ==============================================================================
# 1. CONFIGURAÇÕES GERAIS
# ==============================================================================
LOGO_URL = "https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/SIG_Logo_RGB_Blue.png"

# --- PALETA DE CORES ---
SIG_SKY = "#145efc"     # Azul Principal
TEXT_BLACK = "#000000"  # Preto para Títulos

# ==============================================================================
# 2. FUNÇÕES DE UI
# ==============================================================================
def setup_sidebar():
    """Configura o CSS global e a aparência da barra lateral."""
    st.markdown(
        f"""
        <style>
            /* Oculta elementos nativos desnecessários */
            header, footer, #MainMenu, .st-emotion-cache-h5rgjs {{ visibility: hidden !important; }}
            [data-testid="stSidebarNav"] > ul:first-child > li:first-child {{ display: none !important; }}

            /* Sidebar Travada (Largura Fixa) */
            [data-testid="stSidebar"] {{
                min-width: 300px !important; max-width: 300px !important; width: 300px !important;
                background-color: white !important; border-right: 1px solid #f0f0f0 !important;
            }}
            div[data-testid="stSidebar"] > div:last-child {{ display: none !important; }}

            /* Cabeçalho Personalizado da Sidebar */
            [data-testid="stSidebarNav"]::before {{
                content: "Job Architecture"; display: flex; flex-direction: column; align-items: center; justify-content: flex-end;
                height: 180px; background-image: url('{LOGO_URL}'); background-repeat: no-repeat; background-position: center 10px; background-size: 100px auto;
                color: {TEXT_BLACK} !important; font-size: 1.5rem; font-weight: 900; padding-bottom: 40px; margin-bottom: 20px; border-bottom: 2px solid #f0f2f6;
            }}

            /* --- NAVEGAÇÃO --- */
            [data-testid="stSidebarNav"] > ul {{ padding: 0 15px !important; }}

            /* Estilo Base dos Links */
            [data-testid="stSidebarNav"] li a {{
                background-color: transparent !important;
                color: {TEXT_BLACK} !important;
                font-weight: 500 !important;
                border-radius: 999px !important;
                padding: 10px 24px !important;
                margin-bottom: 5px !important;
                transition: all 0.2s ease-in-out !important;
                border: none !important;
                text-decoration: none !important;
            }}

            /* Limpeza visual (ícones/emojis) */
            [data-testid="stSidebarNav"] li a span:first-child {{ display: none !important; }}
            [data-testid="stSidebarNav"] li a span:last-child {{ display: inline-block !important; }}

            /* Hover (Apenas muda a cor do texto) */
            [data-testid="stSidebarNav"] li a:hover,
            [data-testid="stSidebarNav"] li a:hover span {{
                color: {SIG_SKY} !important;
                background-color: transparent !important;
            }}

            /* ITEM ATIVO (Pílula Azul) */
            ul[data-testid="stSidebarNavItems"] li a[aria-current="page"],
            [data-testid="stSidebarNav"] a[data-active="true"] {{
                background-color: {SIG_SKY} !important;
                color: white !important;
                font-weight: 700 !important;
                box-shadow: 0 2px 4px rgba(20, 94, 252, 0.2) !important;
            }}
            /* Garante texto branco no item ativo mesmo com hover */
            ul[data-testid="stSidebarNavItems"] li a[aria-current="page"]:hover span,
            [data-testid="stSidebarNav"] a[data-active="true"]:hover span {{
                color: white !important;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

def section(title):
    """
    Cria um cabeçalho de secção padronizado para as páginas.
    Uso: section("Título da Secção")
    """
    st.markdown(f"<h1 style='color: {TEXT_BLACK}; font-size: 2.2rem; margin-bottom: 0;'>{title}</h1>", unsafe_allow_html=True)
    st.markdown("---")
