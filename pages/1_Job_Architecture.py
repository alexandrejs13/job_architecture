# -*- coding: utf-8 -*-
# pages/1_Job_Architecture.py

import streamlit as st
from pathlib import Path

# IMPORTS CORRETOS (OPÇÃO A)
from utils.ui import sidebar_logo_and_title

# ======================================================================
# CONFIGURAÇÃO DA PÁGINA
# ======================================================================
st.set_page_config(
    page_title="Job Architecture",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================================
# SIDEBAR SIG UNIFICADA
# ======================================================================
sidebar_logo_and_title(
    logo_path="assets/SIG_Logo_RGB_Black.png",
    active_page="Job Architecture",
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

# ======================================================================
# CSS GLOBAL SIG (TÍTULOS, BOTÕES, CONTAINERS)
# ======================================================================
st.markdown("""
<style>

    /* Fundo da página */
    .main {
        background-color: #ffffff !important;
    }

    /* Títulos (containers azuis SIG) */
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
    }

    /* Container minimalista SIG */
    .sig-container {
        background-color: #ffffff;
        border: 1px solid #e5dfd9;
        padding: 18px 22px;
        border-radius: 6px;
        margin-bottom: 22px;
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
# TÍTULO DA PÁGINA COM ÍCONE PNG (22PX)
# ======================================================================
icon_path = Path("assets/icons/governance.png")

st.markdown(
    f"""
    <div class="sig-title">
        <img src="{icon_path.as_posix()}" width="22px">
        Job Architecture
    </div>
    """,
    unsafe_allow_html=True
)

# ======================================================================
# CONTEÚDO DA PÁGINA
# ======================================================================
st.markdown("""
<div class="sig-container">

### Visão Geral da Arquitetura de Cargos SIG

O módulo **Job Architecture** apresenta a base estrutural do sistema de cargos SIG, 
com diretrizes corporativas, níveis organizacionais, trilhas de carreira, 
princípios de governança e padrões globais de classificação.

Aqui você encontra os componentes fundamentais que sustentam:

- Estrutura de famílias
- Estrutura de níveis (Bands / Grades)
- Descrições de cargo
- Mapas de carreira
- Regras de governança
- Modelos de progressão horizontal e vertical

Use o menu lateral para navegar pelos módulos complementares.

</div>
""", unsafe_allow_html=True)
