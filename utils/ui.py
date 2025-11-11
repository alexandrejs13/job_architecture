def sidebar_logo_and_title():
    logo_url = "https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/SIG_Logo_RGB_Blue.png"

    st.sidebar.markdown(f"""
    <style>
        /* === Estrutura do menu lateral === */
        [data-testid="stSidebarNav"] {{
            margin-top: 160px !important; /* espaço pro header fixo */
            border-top: none !important;
            padding-top: 1rem !important;
        }}

        /* === Header fixo centralizado dentro da sidebar === */
        .sidebar-header {{
            position: fixed;
            top: 0;
            left: 0;
            width: 300px; /* mesma largura padrão da sidebar */
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            background-color: #ffffff;
            padding: 25px 10px 12px 10px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            z-index: 100;
        }}

        .sidebar-header img {{
            width: 120px;
            margin-bottom: 8px;
            opacity: 0.95;
        }}

        .sidebar-header h2 {{
            color: #145efc;
            font-size: 1.3rem;
            font-weight: 800;
            margin: 0;
        }}
    </style>

    <div class="sidebar-header">
        <img src="{logo_url}" alt="SIG Logo">
        <h2>Job Architecture</h2>
    </div>
    """, unsafe_allow_html=True)
