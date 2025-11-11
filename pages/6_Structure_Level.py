# -*- coding: utf-8 -*-
# pages/6_Structure_Level.py

import streamlit as st
import pandas as pd
from pathlib import Path
# Importa a função de carregamento específica do usuário
from utils.data_loader import load_level_structure_df
# Importa a nossa função de visual global
from utils.ui import setup_sidebar
import html

# ===========================================================
# 4. DADOS (FUNÇÕES DE CARREGAMENTO)
# ===========================================================
@st.cache_data 
def load_level_data():
    try:
        df = load_level_structure_df()
        
        if not df.empty:
            df.columns = df.columns.str.strip()
            df = df.fillna('-')
            
            if 'Global Grade' in df.columns:
                # Remove o '.0' de Global Grade e converte para string
                df['Global Grade'] = pd.to_numeric(
                    df['Global Grade'].astype(str).str.replace(r'\.0$', '', regex=True), 
                    errors='coerce'
                ).fillna('-').astype(str).str.replace(r'\.0$', '', regex=True)
            
        return df
    except NameError:
        st.error("Erro: A função `load_level_structure_df()` não foi encontrada.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao carregar dados de nível: {e}")
        return pd.DataFrame()


# ===========================================================
# 1. CONFIGURAÇÃO DE PÁGINA (ÍCONE DE ENGRENAGEM PARA ALINHAMENTO)
# ===========================================================
st.set_page_config(
    page_title="Structure Level", 
    page_icon="⚙️", # ÍCONE: Engrenagem para alinhamento da sidebar
    layout="wide", 
    initial_sidebar_state="expanded"
)

# ===========================================================
# 2. APLICA VISUAL GLOBAL E SIDEBAR
# ===========================================================
setup_sidebar() 

# ===========================================================
# 3. CSS PADRÃO
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

/* Destaque para a tabela executiva */
[data-testid="stDataFrame"] {
    border: 1px solid #ddd;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)

# ===========================================================
# 5. CONTEÚDO PRINCIPAL E TABELA
# ===========================================================

# Renderiza o header padrão (ÍCONE process.png)
st.markdown(f"""
<div class="page-header">
  <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/process.png" alt="icon">
  Estrutura de Níveis (Levels)
</div>
""", unsafe_allow_html=True)

st.markdown("### 📋 Tabela Executiva de Níveis Estruturais")
st.markdown("A tabela a seguir apresenta os níveis, faixas de carreira e Grades Globais (*Global Grades*) definidos na arquitetura.")

# Carrega os dados
df = load_level_data()

if df.empty:
    st.warning("Não foi possível carregar os dados de Nível.")
    st.stop()

# Exibe a tabela simples
st.dataframe(df, use_container_width=True, hide_index=True) 
st.caption(f"Total de níveis estruturais carregados: **{len(df)}** | Total de colunas: **{len(df.columns)}**")
