import streamlit as st

# ===========================================================
# 1) LOGO + TÍTULO FIXOS NA SIDEBAR (acima do menu)
#    -> Usa position: sticky para ficar DENTRO da sidebar
# ===========================================================
def sidebar_logo_and_title():
    logo_url = "https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/SIG_Logo_RGB_Blue.png"

    st.sidebar.markdown(f"""
    <style>
        /* Cabeçalho da sidebar (fica acima do menu e gruda no topo) */
        [data-testid="stSidebar"] .sidebar-header {{
            position: sticky;
            top: 0;
            background: #ffffff;
            z-index: 999;
            padding: 18px 14px 12px 14px;
            border-bottom: 1px solid rgba(0,0,0,0.08);
        }}
        [data-testid="stSidebar"] .sidebar-header img {{
            display: block;
            width: 120px;
            margin: 0 auto 6px auto;
            opacity: 0.98;
        }}
        [data-testid="stSidebar"] .sidebar-header h2 {{
            margin: 0;
            text-align: center;
            font-weight: 800;
            font-size: 1.35rem; /* maior como você pediu */
            color: #145efc;
            letter-spacing: .2px;
        }}

        /* O menu começa logo abaixo do header, sem empurrar demais */
        [data-testid="stSidebarNav"] {{
            margin-top: 6px !important;
            padding-top: 8px !important;
        }}
    </style>

    <div class="sidebar-header">
        <img src="{logo_url}" alt="SIG Logo">
        <h2>Job Architecture</h2>
    </div>
    """, unsafe_allow_html=True)


# ===========================================================
# 2) CABEÇALHO (ícone + título) PARA CADA PÁGINA
# ===========================================================
def header(title: str, icon_url: str | None = None):
    """
    Exibe um cabeçalho consistente no topo da página (fora da sidebar).
    Passe icon_url ABSOLUTO (ex: raw.githubusercontent...) para evitar redirecionamentos.
    """
    icon_html = (
        f'<img src="{icon_url}" width="32" style="vertical-align:middle; margin-right:10px;">'
        if icon_url else ""
    )

    st.markdown(f"""
        <div style="display:flex; align-items:center; margin: 8px 0 10px 0;">
            {icon_html}
            <h1 style="
                margin: 0;
                font-size: 1.9rem;
                font-weight: 800;
                color: #0d47a1;
            ">{title}</h1>
        </div>
        <hr style="border:1px solid rgba(0,0,0,0.1); margin: 6px 0 18px 0;">
    """, unsafe_allow_html=True)
