import streamlit as st
import pandas as pd
from utils.data_loader import load_level_structure_df
# Importa a nossa função de visual global
from utils.ui import setup_sidebar

# ===========================================================
# 1. CONFIGURAÇÃO DE PÁGINA
# ===========================================================
st.set_page_config(page_title="🏗️ Structure Level", layout="wide")

# ===========================================================
# 2. APLICA O VISUAL GLOBAL (Barra Branca + Logo Azul)
# ===========================================================
setup_sidebar()

# ===========================================================
# 3. ESTILOS DA PÁGINA
# ===========================================================
st.markdown("""
<style>
h1 { color: #145efc; font-weight: 800; } /* Atualizado para o Azul SIG Sky exato */
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
