import streamlit as st

def sidebar_logo_and_title():
    logo_url = "https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/SIG_Logo_RGB_Blue.png"

    st.sidebar.markdown(f"""
    <style>
        /* === Estrutura da barra lateral === */
        [data-testid="stSidebarNav"] {{
            margin-top: 180px !important; /* empurra o menu pra baixo */
            border-top: 2px solid rgba(0,0,0,0.08);
            padding-top: 1rem !important;
        }}

        /* === Logo e título fixos acima do menu === */
        .sidebar-header {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            text-align: center;
            background-color: #ffffff;
            padding-top: 25px;
            padding-bottom: 12px;
            z-index: 100;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        }}
        .sidebar-header img {{
            width: 120px;
            opacity: 0.95;
            margin-bottom: 6px;
        }}
        .sidebar-header h2 {{
            color: #145efc;
            font-size: 1.2rem;
            font-weight: 800;
            margin: 0;
        }}
    </style>

    <div class="sidebar-header">
        <img src="{logo_url}" alt="SIG Logo">
        <h2>Job Architecture</h2>
    </div>
    """, unsafe_allow_html=True)
