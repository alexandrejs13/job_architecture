import streamlit as st

# ===========================================================
# 1. LOGO + TÍTULO FIXOS ACIMA DO MENU
# ===========================================================
def sidebar_logo_and_title():
    logo_url = "https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/SIG_Logo_RGB_Blue.png"

    st.sidebar.markdown(f"""
    <style>
        /* === Cabeçalho fixo dentro da sidebar === */
        section[data-testid="stSidebar"] div[data-testid="stSidebarNav"]::before {{
            content: "";
            display: block;
            background-color: #fff;
            border-bottom: 1px solid rgba(0, 0, 0, 0.1);
            text-align: center;
            padding: 22px 12px 14px 12px;
            position: sticky;
            top: 0;
            z-index: 999;
            background-image: url('{logo_url}');
            background-repeat: no-repeat;
            background-position: center 6px;
            background-size: 110px;
        }}
        section[data-testid="stSidebar"] div[data-testid="stSidebarNav"]::after {{
            content: "Job Architecture";
            display: block;
            text-align: center;
            color: #145efc;
            font-weight: 800;
            font-size: 1.35rem;
            margin-top: 110px;
            margin-bottom: 12px;
        }}
    </style>
    """, unsafe_allow_html=True)


# ===========================================================
# 2. HEADER AZUL NAS PÁGINAS
# ===========================================================
def header(title: str, icon_url: str | None = None):
    """
    Exibe o header azul com ícone e título.
    O ícone deve usar URL absoluta (RAW do GitHub).
    """
    icon_html = f'<img src="{icon_url}" width="28" style="vertical-align:middle; margin-right:10px;">' if icon_url else ""

    st.markdown(f"""
    <div style="
        background-color: #2962ff;
        color: white;
        padding: 14px 22px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        margin-bottom: 28px;
    ">
        {icon_html}
        <span style="font-size:1.5rem; font-weight:800;">{title}</span>
    </div>
    """, unsafe_allow_html=True)
