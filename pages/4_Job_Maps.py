# -*- coding: utf-8 -*-
# pages/4_Job_Maps.py

import streamlit as st
import pandas as pd
from pathlib import Path

# IMPORTS CORRETOS (OPÇÃO A)
from utils.ui import sidebar_logo_and_title
from utils.data_loader import load_excel_data

# =============================================================================
# CONFIGURAÇÃO DA PÁGINA
# =============================================================================
st.set_page_config(
    page_title="Job Maps",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# SIDEBAR SIG UNIFICADA
# =============================================================================
sidebar_logo_and_title(
    logo_path="assets/SIG_Logo_RGB_Black.png",
    active_page="Job Maps",
    menu_items=[
        ("Job Architecture", "governance.png", "1_Job_Architecture.py"),
        ("Job Families", "people employees.png", "2_Job_Families.py"),
        ("Job Profile Description", "business review clipboard.png", "3_Job_Profile_Description.py"),
        ("Job Maps", "globe trade.png", "4_Job_Maps.py"),
        ("Job Match (GGS)", "checkmark success.png", "5_Job_Match.py"),
        ("Structure Level", "process.png", "6_Structure_Level.py"),
        ("Dashboard", "data 2 performance.png", "7_Dashboard.py"),
    ],
    icons_path="assets/icons",
    pilula_color="#145efc",
    sidebar_bg="#f2efeb",
    text_color="#000000",
)

# =============================================================================
# CSS SIG UNIFICADO
# =============================================================================
st.markdown("""
<style>

    /* Fundo da página */
    .main {
        background-color: #ffffff !important;
    }

    /* Títulos SIG */
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
        margin-top: 8px;
    }

    /* Container minimalista */
    .sig-container {
        background-color: #ffffff;
        border: 1px solid #e5dfd9;
        padding: 18px 22px;
        border-radius: 6px;
        margin-bottom: 20px;
    }

    /* Botões SIG */
    .stButton>button {
        background-color: #145efc !important;
        color: white !important;
        border-radius: 6px !important;
        padding: 8px 16px !important;
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
icon_path = Path("assets/icons/globe trade.png")

st.markdown(
    f"""
    <div class="sig-title">
        <img src="{icon_path.as_posix()}" width="22px">
        Job Maps
    </div>
    """,
    unsafe_allow_html=True
)

# =============================================================================
# CARREGAR DADOS
# =============================================================================
job_families_path = Path("data/Job Family.xlsx")
structure_levels_path = Path("data/Level Structure.xlsx")

df_families = load_excel_data(job_families_path)
df_levels = load_excel_data(structure_levels_path)

if df_families is None or df_levels is None:
    st.error("Erro ao carregar dados necessários (Job Family ou Level Structure).")
    st.stop()

# =============================================================================
# SEÇÃO PRINCIPAL
# =============================================================================
st.markdown(
    """
<div class="sig-container">
    <h3>Mapeamento Estrutural de Cargos</h3>
    Explore abaixo a integração entre Family, Sub-Family e Níveis (Bands / Grades)
    conforme a Arquitetura de Cargos SIG.
</div>
""",
    unsafe_allow_html=True
)

# =============================================================================
# SELEÇÃO DE FAMILY → CARREGA SUB-FAMILY E NÍVEIS
# =============================================================================
families = sorted(df_families["Family"].dropna().unique().tolist())

family_selected = st.selectbox("Selecione uma Job Family", families)

if family_selected:
    df_filtered = df_families[df_families["Family"] == family_selected]

    sub_families = sorted(df_filtered["Sub-Family"].dropna().unique().tolist())
    sub_selected = st.selectbox("Selecione uma Sub-Family", sub_families)

    if sub_selected:
        df_sub = df_filtered[df_filtered["Sub-Family"] == sub_selected]

        st.markdown(
            """
            <div class="sig-container">
                <h4>Mapa Estrutural</h4>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.dataframe(df_sub, use_container_width=True)

# =============================================================================
# NÍVEIS ORGANIZACIONAIS (EXIBIÇÃO RESUMIDA)
# =============================================================================
st.markdown(
    """
<div class="sig-container">
    <h3>Níveis Organizacionais – Referência</h3>
    Abaixo, apresentamos a estrutura de Bands / Grades utilizada na Arquitetura SIG.
</div>
""",
    unsafe_allow_html=True
)

st.dataframe(df_levels, use_container_width=True)
