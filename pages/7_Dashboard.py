# -*- coding: utf-8 -*-
# pages/7_Dashboard.py

import streamlit as st
from pathlib import Path
import pandas as pd

# IMPORT CORRETO (OPÇÃO A)
from utils.ui import sidebar_logo_and_title

# =============================================================================
# CONFIGURAÇÃO DA PÁGINA
# =============================================================================
st.set_page_config(
    page_title="Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# SIDEBAR SIG UNIFICADA
# =============================================================================
sidebar_logo_and_title(
    logo_path="assets/SIG_Logo_RGB_Black.png",
    active_page="Dashboard",
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
# CSS SIG UNIFICADO
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
        margin-bottom: 20px;
        margin-top: 10px;
    }

    .sig-container {
        background-color: #ffffff;
        border: 1px solid #e5dfd9;
        padding: 18px 22px;
        border-radius: 6px;
        margin-bottom: 22px;
    }

    .metric-box {
        background-color: #ffffff;
        border: 1px solid #e5dfd9;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
        margin-bottom: 14px;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #145efc;
        margin-bottom: 4px;
    }

    .metric-label {
        font-size: 14px;
        color: #555;
    }

</style>
""", unsafe_allow_html=True)

# =============================================================================
# TÍTULO COM ÍCONE
# =============================================================================
icon_path = Path("assets/icons/data 2 performance.png")

st.markdown(
    f"""
    <div class="sig-title">
        <img src="{icon_path.as_posix()}" width="22px">
        Dashboard
    </div>
    """,
    unsafe_allow_html=True
)

# =============================================================================
# CARREGAMENTO DE DADOS NECESSÁRIOS
# =============================================================================
try:
    df_families = pd.read_excel("data/Job Family.xlsx")
    df_levels = pd.read_excel("data/Level Structure.xlsx")
    df_profiles = pd.read_excel("data/Job Profile.xlsx")
except Exception:
    df_families = df_levels = df_profiles = None

# =============================================================================
# MÉTRICAS PRINCIPAIS
# =============================================================================
st.markdown("<div class='sig-container'><h3>Métricas Consolidadas</h3></div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
    st.markdown("<div class='metric-value'>✔️</div>", unsafe_allow_html=True)
    st.markdown("<div class='metric-label'>Aplicação SIG Ativa</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    total_families = len(df_families["Family"].unique()) if df_families is not None else "-"
    st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-value'>{total_families}</div>", unsafe_allow_html=True)
    st.markdown("<div class='metric-label'>Job Families</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    total_profiles = len(df_profiles) if df_profiles is not None else "-"
    st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-value'>{total_profiles}</div>", unsafe_allow_html=True)
    st.markdown("<div class='metric-label'>Perfis de Cargo</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# =============================================================================
# TABELAS OPCIONAIS
# =============================================================================
st.markdown("""
<div class="sig-container">
<h3>Dados Consolidados</h3>
Selecione abaixo qual conjunto de dados deseja visualizar.
</div>
""", unsafe_allow_html=True)

option = st.selectbox(
    "Selecione o dataset:",
    ["Job Families", "Job Profiles", "Structure Levels"]
)

if option == "Job Families" and df_families is not None:
    st.dataframe(df_families, use_container_width=True)

elif option == "Job Profiles" and df_profiles is not None:
    st.dataframe(df_profiles, use_container_width=True)

elif option == "Structure Levels" and df_levels is not None:
    st.dataframe(df_levels, use_container_width=True)
