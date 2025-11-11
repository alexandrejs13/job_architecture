import streamlit as st

# ===========================================================
# 1. LOGO E TÍTULO FIXOS NA SIDEBAR
# ===========================================================
def sidebar_logo_and_title():
    logo_url = "https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/SIG_Logo_RGB_Blue.png"

    st.sidebar.markdown(f"""
    <style>
        /* --- Container do logo fixo no topo da sidebar --- */
        [data-testid="stSidebar"] {{
            padding-top: 0 !important;
        }}
        [data-testid="stSidebarNav"] {{
            margin-top: 165px !important; /* espaço para o header */
        }}
        .sidebar-top {{
            position: fixed;
            top: 0;
            left: 0;
            width: inherit;
            background: #ffffff;
            text-align: center;
            padding: 22px 8px 12px 8px;
            border-bottom: 1px solid rgba(0,0,0,0.1);
            z-index: 999;
        }}
        .sidebar-top img {{
            width: 110px;
            opacity: 0.96;
            margin-bottom: 4px;
        }}
        .sidebar-top h2 {{
            color: #145efc;
            font-size: 1.35rem;
            font-weight: 800;
            margin: 0;
        }}
    </style>

    <div class="sidebar-top">
        <img src="{logo_url}" alt="SIG Logo">
        <h2>Job Architecture</h2>
    </div>
    """, unsafe_allow_html=True)


# ===========================================================
# 2. HEADER AZUL DA PÁGINA
# ===========================================================
def header(title: str, icon_url: str | None = None):
    """
    Header azul padronizado com ícone PNG remoto.
    """
    icon_html = ""
    if icon_url:
        icon_html = f'<img src="{icon_url}" width="28" style="margin-right:10px; vertical-align:middle;">'

    st.markdown(f"""
    <div style="
        display: flex;
        align-items: center;
        background-color: #2962ff;
        color: white;
        padding: 14px 20px;
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        margin-bottom: 26px;
    ">
        {icon_html}
        <span style="font-size:1.5rem; font-weight:800;">{title}</span>
    </div>
    """, unsafe_allow_html=True)
