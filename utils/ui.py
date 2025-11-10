import streamlit as st

def setup_sidebar():
    """
    Configura o estilo visual da barra lateral (sidebar) e do menu,
    aplicando a identidade visual da SIG.
    """
    
    # Cores SIG para a sidebar
    SIDEBAR_BG = "#f2efeb"  # SIG Sand 1
    SIDEBAR_TEXT = "#333333"
    LINK_COLOR = "#145efc"  # SIG Sky

    st.markdown(f"""
    <style>
        /* Cor de fundo da sidebar */
        [data-testid="stSidebar"] {{
            background-color: {SIDEBAR_BG};
        }}
        
        /* Ajuste de texto na sidebar */
        [data-testid="stSidebar"] .stMarkdown p, 
        [data-testid="stSidebar"] .stMarkdown li {{
            color: {SIDEBAR_TEXT};
        }}

        /* Estilo dos links de navegação padrão (caso visíveis) */
        section[data-testid="stSidebar"] a {{
            color: {LINK_COLOR} !important;
        }}

        /* Esconde decorações padrão do Streamlit que podem poluir o visual */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        
        /* (Opcional) Ajuste fino do padding da sidebar */
        .css-1d391kg {{
            padding-top: 2rem;
        }}
    </style>
    """, unsafe_allow_html=True)

    # (Opcional) Header da Sidebar
    # st.sidebar.image("caminho_para_logo_sig.png", use_column_width=True)
    st.sidebar.markdown("### 🏛️ Job Architecture")
    st.sidebar.markdown("---")
