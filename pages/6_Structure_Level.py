# -*- coding: utf-8 -*-
# pages/6_Structure_Level.py

import streamlit as st
import pandas as pd
from pathlib import Path
from utils.ui import sidebar_logo_and_title

# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(
    page_title="Structure Level",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Logo SIG na sidebar
sidebar_logo_and_title("assets/SIG_Logo_RGB_Black.png")

# ==========================================================
# TÍTULO SIG
# ==========================================================

st.markdown("""
<div class="sig-title">
    <img src="assets/icons/process.png">
    <span>Structure Level</span>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# VISÃO GERAL
# ==========================================================

st.markdown("""
<div class="sig-card">
    <h3>Visão Geral</h3>
    <p>
        A Estrutura de Níveis (Structure Level) organiza os cargos com base nas
        faixas de contribuição, escopo e responsabilidade. Esta estrutura é
        fundamental para garantir consistência global, alinhamento transversal
        entre funções e suporte às trilhas de carreira.
    </p>
    <p>
        Abaixo você pode visualizar todos os níveis cadastrados, conforme metodologia
        corporativa SIG e alinhamento com os Career Bands e Global Grades.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# CARREGAMENTO DO ARQUIVO
# ==========================================================

file_path = Path("data/Level Structure.xlsx")

if not file_path.exists():
    st.error("Arquivo 'Level Structure.xlsx' não encontrado na pasta data/")
    st.stop()

df = pd.read_excel(file_path)

# ==========================================================
# EXIBIÇÃO DA ESTRUTURA
# ==========================================================

st.markdown("""
<div class="sig-card">
    <h3>Estrutura Completa de Níveis</h3>
</div>
""", unsafe_allow_html=True)

st.dataframe(df, use_container_width=True)

# ==========================================================
# RODAPÉ
# ==========================================================

st.markdown("""
<div class="sig-card">
    <p style="font-size:14px; color:#666;">
        Utilize o menu lateral para acessar o Dashboard consolidado ou retornar a outras seções da arquitetura.
    </p>
</div>
""", unsafe_allow_html=True)
