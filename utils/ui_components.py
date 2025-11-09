import streamlit as st

# ===========================================================
# 🔹 COMPONENTES DE INTERFACE PADRONIZADOS
# ===========================================================

def section(title: str):
    """
    Renderiza um título de seção com espaçamento visual consistente.
    """
    st.markdown(
        f"""
        <h1 style='display:flex;align-items:center;gap:10px;
        margin-top:-10px;margin-bottom:25px;
        font-size:1.9rem;color:#145efc;font-weight:800;'>
        {title}</h1>
        """,
        unsafe_allow_html=True
    )

def lock_sidebar():
    """
    Impede o usuário de redimensionar a sidebar e mantém largura fixa.
    """
    st.markdown("""
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] {
        width: 300px !important;
        min-width: 300px !important;
        max-width: 300px !important;
    }
    [data-testid="stSidebarCollapsedControl"] {
        width: 300px !important;
    }
    </style>
    """, unsafe_allow_html=True)
