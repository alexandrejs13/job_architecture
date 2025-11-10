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

# --- Conteúdo da Página ---
st.markdown("""
# 🧭 Job Architecture Explorer

Bem-vindo ao painel de cargos corporativos.

Use o menu lateral para acessar as ferramentas disponíveis, como:
- **🧠 Find My Job Profile** (busca semântica de cargos)
- **📊 Comparativo de Cargos Selecionados** (comparação detalhada)
- **📚 Tabelas de Arquitetura de Cargos** (estrutura completa)

---
""")
