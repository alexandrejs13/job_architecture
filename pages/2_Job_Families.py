# -*- coding: utf-8 -*-
# pages/2_Job_Families.py

import streamlit as st
from pathlib import Path
import pandas as pd

# IMPORTS CORRETOS (OPÇÃO A)
from utils.ui import sidebar_logo_and_title
from utils.data_loader import load_excel_data

# ======================================================================
# CONFIGURAÇÃO DA PÁGINA
# ======================================================================
st.set_page_config(
    page_title="Job Families",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================================
# SIDEBAR SIG UNIFICADA
# ======================================================================
sidebar_logo_and_title(
    logo_path="assets/SIG_Logo_RGB_Black.png",
    active_page="Job Families",
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

# ======================================================================
# CSS GLOBAL SIG
# ======================================================================
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
        margin-top: 10px;
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

# ======================================================================
# TÍTULO COM ÍCONE PNG
# ======================================================================
icon_path = Path("assets/icons/people employees.png")

st.markdown(
    f"""
    <div class="sig-title">
        <img src="{icon_path.as_posix()}" width="22px">
        Job Families
    </div>
    """,
    unsafe_allow_html=True
)

# ======================================================================
# CARREGAR DADOS
# ======================================================================
job_families_path = Path("data/Job Family.xlsx")
df = load_excel_data(job_families_path)

# ======================================================================
# CONTEÚDO
# ======================================================================

st.markdown(
    """
<div class="sig-container">
    <h3>Consulta de Job Families</h3>
    Utilize a tabela abaixo para explorar as Job Families oficiais do SIG, incluindo:
    <ul>
        <li>Famílias de cargo</li>
        <li>Sub-famílias</li>
        <li>Descrições gerais</li>
        <li>Áreas organizacionais</li>
    </ul>
</div>
""",
    unsafe_allow_html=True
)

# TABELA
st.dataframe(df, use_container_width=True)
