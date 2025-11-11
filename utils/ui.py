import streamlit as st

# ===========================================================
# 1️⃣ FUNÇÃO: LOGO E TÍTULO NA BARRA LATERAL
# ===========================================================
def sidebar_logo_and_title():
    logo_url = "https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/SIG_Logo_RGB_Blue.png"
    st.sidebar.markdown(f"""
    <style>
        /* Oculta o item "app" do menu lateral */
        [data-testid="stSidebarNav"] ul li:first-child {{
            display: none !important;
        }}

        /* Espaçamento para exibir logo */
        [data-testid="stSidebarNav"] {{
            padding-top: 150px !important;
        }}

        /* Header do logo */
        .sidebar-header {{
            position: absolute;
            top: 20px;
            left: 0;
            width: 100%;
            text-align: center;
        }}
        .sidebar-header img {{
            width: 110px;
            opacity: 0.95;
            margin-bottom: 4px;
        }}
        .sidebar-header h2 {{
            color: #145efc;
            font-size: 1rem;
            font-weight: 700;
            margin: 0;
        }}
    </style>

    <div class="sidebar-header">
        <img src="{logo_url}" alt="SIG Logo">
        <h2>Job Architecture</h2>
    </div>
    """, unsafe_allow_html=True)

# ===========================================================
# 2️⃣ FUNÇÃO: CABEÇALHO AZUL COM ÍCONE
# ===========================================================
def header(title: str, icon_filename: str):
    """Cria o cabeçalho azul SIG com ícone"""
    icon_url = f"https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/{icon_filename}"

    st.markdown(f"""
    <style>
        .header-bar {{
            display: flex;
            align-items: center;
            background-color: #145efc;
            padding: 0.8rem 1.2rem;
            border-radius: 12px;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        }}
        .header-bar img {{
            width: 28px;
            height: 28px;
            margin-right: 10px;
        }}
        .header-title {{
            font-size: 1.4rem;
            font-weight: 700;
        }}
    </style>
    <div class="header-bar">
        <img src="{icon_url}" alt="icon">
        <div class="header-title">{title}</div>
    </div>
    """, unsafe_allow_html=True)
