# -*- coding: utf-8 -*-
# pages/6_Structure_Level.py

import streamlit as st
import pandas as pd
from pathlib import Path
# Importa a função de carregamento específica do usuário
from utils.data_loader import load_level_structure_df, load_excel_data 
# Importa a nossa função de visual global
from utils.ui import setup_sidebar, sidebar_logo_and_title
import html

# ===========================================================
# 4. DADOS (FUNÇÕES DE CARREGAMENTO)
# ===========================================================
# Mantendo apenas o essencial para a tabela
@st.cache_data 
def load_level_data():
    try:
        # Carrega a tabela de estrutura de níveis usando a função do usuário
        df = load_level_structure_df()
        # Limpeza básica (opcional, mas seguro)
        if not df.empty:
            df.columns = df.columns.str.strip()
            df = df.fillna('-')
        return df
    except NameError:
        st.error("Erro: A função `load_level_structure_df()` não foi encontrada. Verifique o arquivo `utils/data_loader.py`.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao carregar dados de nível: {e}")
        return pd.DataFrame()


# ===========================================================
# 1. CONFIGURAÇÃO DE PÁGINA
# ===========================================================
st.set_page_config(
    page_title="Structure Level", 
    page_icon="🪜", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# ===========================================================
# 2. APLICA VISUAL GLOBAL E SIDEBAR
# ===========================================================
setup_sidebar()

# ===========================================================
# 3. CSS PADRÃO (Apenas o necessário para o header)
# ===========================================================
st.markdown("""
<style>
:root {
    --blue: #145efc;
}

/* ============ HEADER PADRÃO ============ */
.page-header {
    background-color: var(--blue);
    color: white;
    font-weight: 750;
    font-size: 1.35rem;
    border-radius: 12px;
    padding: 22px 36px;
    display: flex;
    align-items: center;
    gap: 18px;
    width: 100%;
    margin-bottom: 40px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.page-header img { width: 48px; height: 48px; }

/* Neutraliza o h1 original */
h1 { display: none !important; }

</style>
""", unsafe_allow_html=True)

# ===========================================================
# 5. CONTEÚDO PRINCIPAL E TABELA
# ===========================================================

# Renderiza o header padrão
st.markdown(f"""
<div class="page-header">
  <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/governance.png" alt="icon">
  Estrutura de Níveis (Levels)
</div>
""", unsafe_allow_html=True)

st.markdown("### 📋 Tabela de Níveis Estruturais")

# Carrega os dados
df = load_level_data()

if df.empty:
    st.warning("Não foi possível carregar os dados de Nível.")
    st.stop()

# Exibe a tabela simples (formato anterior)
st.dataframe(df, use_container_width=True, hide_index=True) 
st.caption(f"Total de níveis estruturais carregados: {len(df)} | Total de colunas de dados: {len(df.columns)}")
