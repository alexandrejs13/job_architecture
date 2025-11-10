import streamlit as st
# --- IMPORTANTE: Importe 'section' aqui para corrigir o erro ---
from utils.ui import setup_sidebar, section

# ==============================================================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="Job Architecture",
    page_icon="🏛️",
    layout="wide"
)

# ==============================================================================
# 2. SETUP UI (CSS GLOBAL)
# ==============================================================================
setup_sidebar()

# ==============================================================================
# 3. CONTEÚDO DA PÁGINA
# ==============================================================================
# Agora esta função vai funcionar porque foi importada acima
section("🏛️ Job Architecture")

st.markdown(
    """
    Esta página é destinada à estruturação da Arquitetura de Cargos.
    
    ### Próximos Passos
    * Definir os níveis hierárquicos.
    * Mapear as famílias de cargos.
    * Estabelecer as trilhas de carreira.
    """
)
