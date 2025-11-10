import streamlit as st
# Outros imports necessários
from utils.ui import setup_sidebar

# 1. Configuração da Página (SEMPRE EM PRIMEIRO se existir)
st.set_page_config(
    page_title="Job Architecture",
    page_icon="🏛️",
    layout="wide"
)

# 2. IMEDIATAMENTE INJETA O CSS
setup_sidebar()

# ===========================================================
# 3. ESTILOS DA PÁGINA
# ===========================================================
st.markdown("""
<style>
    /* O estilo h1 agora é controlado globalmente pelo utils/ui.py */
</style>
""", unsafe_allow_html=True)

# ===========================================================
# 4. CONTEÚDO
# ===========================================================
st.markdown("# 🏗️ Structure Level")

# Carrega os dados
df = load_level_structure_df()

# Exibe a tabela
st.dataframe(df, use_container_width=True, hide_index=True) # hide_index=True geralmente fica mais limpo
st.caption(f"Total de níveis estruturais carregados: {len(df)} | Total de colunas de dados: {len(df.columns)}")
