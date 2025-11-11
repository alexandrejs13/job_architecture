import streamlit as st
from pathlib import Path

# ===========================================================
# Função: Ocultar o item "app" do menu lateral padrão
# ===========================================================
def hide_streamlit_menu_item():
    st.markdown("""
    <style>
    /* Remove o item 'app' do topo do menu lateral */
    [data-testid="stSidebarNav"] ul li:first-child {
        display: none !important;
    }

    /* Ajuste de espaçamento superior do menu */
    section[data-testid="stSidebar"] > div:first-child {
        padding-top: 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ===========================================================
# Função: Logo e Título na barra lateral
# ===========================================================
def sidebar_logo_and_title():
    """Exibe o logo SIG e o título Job Architecture acima do menu lateral"""
    logo_path = "https://github.com/alexandrejs13/job_architecture/raw/main/assets/SIG_Logo_RGB_Blue.png"
    st.markdown(f"""
    <style>
        .sidebar-logo {{
            text-align: center;
            margin-top: -10px;
            margin-bottom: 15px;
        }}
        .sidebar-logo img {{
            width: 140px;
            margin-bottom: 4px;
        }}
        .sidebar-logo h2 {{
            font-size: 1.15rem;
            color: #003399;
            font-weight: 700;
            margin: 0;
        }}
    </style>
    <div class="sidebar-logo">
        <img src="{logo_path}" alt="SIG Logo">
        <h2>Job Architecture</h2>
    </div>
    """, unsafe_allow_html=True)

# ===========================================================
# Função: Cabeçalho Azul Padrão
# ===========================================================
def header(title: str, icon_path: str):
    """Cria o cabeçalho azul superior com ícone"""
    icon_full_path = Path(icon_path)
    if not icon_full_path.exists():
        icon_full_path = f"https://github.com/alexandrejs13/job_architecture/raw/main/{icon_path}"

    st.markdown(f"""
    <style>
        .header-bar {{
            display: flex;
            align-items: center;
            background-color: #145efc;
            padding: 0.9rem 1.5rem;
            border-radius: 12px;
            color: white;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        }}
        .header-bar img {{
            width: 28px;
            height: 28px;
            margin-right: 12px;
        }}
        .header-title {{
            font-size: 1.5rem;
            font-weight: 700;
            letter-spacing: 0.5px;
        }}
    </style>
    <div class="header-bar">
        <img src="{icon_full_path}" alt="icon">
        <div class="header-title">{title}</div>
    </div>
    """, unsafe_allow_html=True)
