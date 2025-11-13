# -*- coding: utf-8 -*-
# pages/4_Job_Maps.py

import streamlit as st
import pandas as pd
from pathlib import Path
from utils.ui import sidebar_logo_and_title

# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="Job Maps",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Logo SIG
sidebar_logo_and_title("assets/SIG_Logo_RGB_Black.png")

# ==========================================================
# TÍTULO SIG
# ==========================================================

st.markdown("""
<div class="sig-title">
    <img src="assets/icons/globe trade.png">
    <span>Job Maps</span>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# VISÃO GERAL
# ==========================================================

st.markdown("""
<div class="sig-card">
    <h3>Visão Geral</h3>
    <p>
        Os Job Maps representam a relação visual e hierárquica entre funções,
        subfamílias e níveis organizacionais. Este mapa facilita a compreensão
        das trilhas de carreira, progressões possíveis e conexões entre cargos.
    </p>
    <p>
        Abaixo, você pode visualizar a estrutura extraída do arquivo oficial
        de níveis organizacionais da SIG, considerando Career Bands, Grades
        e Subníveis conforme metodologia global.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# CARREGAR ARQUIVO DE NÍVEIS
# ==========================================================

file_path = Path("data/Level Structure.xlsx")

if not file_path.exists():
    st.error("Arquivo 'Level Structure.xlsx' não encontrado na pasta data/")
    st.stop()

df = pd.read_excel(file_path)

# ==========================================================
# APRESENTAÇÃO DO MAPA
# ==========================================================

st.markdown("""
<div class="sig-card">
    <h3>Mapa de Estrutura Organizacional</h3>
    <p>
        A tabela abaixo apresenta os níveis estruturais, permitindo visualizar
        como cada nível se conecta às Job Families e Job Profiles.
    </p>
</div>
""", unsafe_allow_html=True)

st.dataframe(df, use_container_width=True)

# ==========================================================
# RODAPÉ
# ==========================================================

st.markdown("""
<div class="sig-card">
    <p style="font-size:14px; color:#666;">
        Continue navegando para acessar o Job Match (GGS) e a Estrutura de Níveis (Structure Level).
    </p>
</div>
""", unsafe_allow_html=True)
