# -*- coding: utf-8 -*-
# pages/2_Job_Families.py

import streamlit as st
from utils.ui import sidebar_logo_and_title
from utils.data_loader import load_excel_data
from pathlib import Path
import pandas as pd

# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="Job Families",
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
    <img src="assets/icons/people employees.png">
    <span>Job Families</span>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# CARREGAMENTO DO ARQUIVO
# ==========================================================

file_path = Path("data/Job Family.xlsx")

if not file_path.exists():
    st.error("Arquivo 'Job Family.xlsx' não encontrado na pasta data/")
else:
    df = pd.read_excel(file_path)

    st.markdown("""
    <div class="sig-card">
        <h3>Visão Geral</h3>
        <p>
            As Job Families organizam cargos em agrupamentos lógicos de acordo
            com suas responsabilidades, natureza do trabalho e competências requeridas.
            Essa estrutura facilita mobilidade, planejamento de carreira e governança
            organizacional.
        </p>
        <p>
            Utilize a tabela abaixo para visualizar todas as Job Families, Sub-Families
            e níveis estruturados conforme a metodologia corporativa SIG e alinhamento
            global WTW.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ==========================================================
    # TABELA PRINCIPAL
    # ==========================================================

    st.markdown("""
    <div class="sig-card">
        <h3>Estrutura de Job Families</h3>
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(df, use_container_width=True)

# ==========================================================
# RODAPÉ
# ==========================================================

st.markdown("""
<div class="sig-card">
    <p style="font-size:14px; color:#666;">
        Continue navegando para acessar Job Profile Description, Job Maps
        e a ferramenta de Job Match (GGS).
    </p>
</div>
""", unsafe_allow_html=True)
