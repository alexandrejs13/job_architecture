import streamlit as st

# ===========================================================
# ✅ Componente visual padrão para títulos de seção
# ===========================================================
def section(title: str):
    """
    Renderiza um título de seção com ícone e espaçamento visual padronizado.
    """
    st.markdown(f"""
        <h1 style="
            display:flex;
            align-items:center;
            gap:10px;
            font-size:1.7rem;
            font-weight:800;
            color:#1E56E0;
            margin-top:0.8rem;
            margin-bottom:1.8rem;
        ">
            {title}
        </h1>
    """, unsafe_allow_html=True)
