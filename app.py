import streamlit as st
# Importa a função de visual que criamos em utils/ui.py
from utils.ui import setup_sidebar

# --- Configuração Inicial da Página (PRIMEIRO COMANDO SEMPRE) ---
st.set_page_config(
    page_title="Job Architecture Explorer",
    page_icon="🧭",
    layout="wide"
)

# --- Aplica o Visual (SEGUNDO COMANDO) ---
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
