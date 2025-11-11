# -*- coding: utf-8 -*-
# pages/6_Structure_Level.py

import streamlit as st
import pandas as pd
from pathlib import Path
from utils.data_loader import load_level_structure_df
from utils.ui import sidebar_logo_and_title # Importação alterada
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
# 1. CONFIGURAÇÃO DE PÁGINA
# ===========================================================
st.set_page_config(
    page_title="Structure Level", 
    page_icon="⚙️", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# ===========================================================
# 2. APLICA VISUAL GLOBAL E SIDEBAR
# ===========================================================
sidebar_logo_and_title() # Chamada de função alterada

# ===========================================================
# 3. CSS PADRÃO E INJEÇÃO DE ÍCONE NA SIDEBAR
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
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

/* ============ CORREÇÃO: INJEÇÃO FORÇADA DO ÍCONE NA SIDEBAR ============ */
/* Seleciona o item da sidebar com o texto 'Structure Level' */
[data-testid="stSidebarNav"] li a[href*="Structure_Level"]::before {
    /* O ícone já existe aqui (ex: Job Maps), mas está fora de ordem. 
       Vamos forçar um novo ícone para garantir a visualização correta. */
    content: "⚙️ ";
    margin-right: 6px; 
    font-size: 1.2em;
    vertical-align: middle;
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
