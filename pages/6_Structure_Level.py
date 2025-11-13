# -*- coding: utf-8 -*-
# pages/6_Structure_Level.py

import streamlit as st
from pathlib import Path
import pandas as pd

# IMPORTS CORRETOS (OPÇÃO A)
from utils.ui import sidebar_logo_and_title
from utils.data_loader import load_excel_data

# =============================================================================
# CONFIGURAÇÃO DA PÁGINA
# =============================================================================
st.set_page_config(
    page_title="Structure Level",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# SIDEBAR SIG UNIFICADA
# =============================================================================
sidebar_logo_and_title(
    logo_path="assets/SIG_Logo_RGB_Black.png",
    active_page="Structure Level",
    menu_items=[
        ("Job Architecture", "governance.png", "1_Job_Architecture.py"),
        ("Job Families", "people employees.png", "2_Job_Families.py"),
        ("Job Profile Description", "business review clipboard.png", "3_Job_Profile_Description.py"),
        ("Job Maps", "globe trade.png", "4_Job_Maps.py"),
        ("Job Match (GGS)", "checkmark success.png", "5_Job_Match.py"),
        ("Structure Level", "process.png", "6_Structure_Level.py"),
        ("Dashboard", "data 2 performance.png", "7_Dashboard.py"),
    ],
)

# =============================================================================
# CSS GLOBAL SIG — PÁGINA BRANCA, TÍTULOS AZUIS, CONTAINERS MINIMALISTAS
# =============================================================================
st.markdown("""
<style>

    .main {
        background-color: #ffffff !important;
    }

    .sig-title {
        background-color: #145efc;
        color: white;
        padding: 14px 20px;
        border-radius: 6px;
        font-size: 22px;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 18px;
        margin-top: 10px;
    }

    .sig-container {
        background-color: #ffffff;
        border: 1px solid #e5dfd9;
        padding: 18px 22px;
        border-radius: 6px;
        margin-bottom: 20px;
    }

    .stButton>button {
        background-color: #145efc !important;
        color: white !important;
        border-radius: 6px !important;
        padding: 10px 18px !important;
        font-weight: 600 !important;
        border: none !important;
    }
    .stButton>button:hover {
        background-color: #0f4cd4 !important;
    }

</style>
""", unsafe_allow_html=True)

# =============================================================================
# TÍTULO COM ÍCONE
# =============================================================================
icon_path = Path("assets/icons/process.png")

st.markdown(
    f"""
    <div class="sig-title">
        <img src="{icon_path.as_posix()}" width="22px">
        Structure Level
    </div>
    """,
    unsafe_allow_html=True
)

# =============================================================================
# CARREGAMENTO DA ESTRUTURA DE NÍVEIS
# =============================================================================
data_path = Path("data/Level Structure.xlsx")
df = load_excel_data(data_path)

if df is None or df.empty:
    st.error("Erro ao carregar Level Structure.xlsx")
    st.stop()

# =============================================================================
# SEÇÃO DESCRITIVA
# =============================================================================
st.markdown("""
<div class="sig-container">
    <h3>Modelo de Níveis Organizacionais SIG</h3>
    Abaixo são apresentados os níveis estruturais utilizados na arquitetura global SIG,
    incluindo Career Bands, Grades, escopos e diferenciação hierárquica.
</div>
""", unsafe_allow_html=True)

# =============================================================================
# TABELA
# =============================================================================
st.dataframe(df, use_container_width=True)
