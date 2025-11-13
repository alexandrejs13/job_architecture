# -*- coding: utf-8 -*-
# pages/3_Job_Profile_Description.py

import streamlit as st
import pandas as pd
import re
from pathlib import Path
import html

# IMPORTS CORRETOS (OPÇÃO A)
from utils.ui import sidebar_logo_and_title
from utils.data_loader import load_excel_data

# =============================================================================
# CONFIGURAÇÃO DA PÁGINA
# =============================================================================
st.set_page_config(
    page_title="Job Profile Description",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# SIDEBAR SIG UNIFICADA
# =============================================================================
sidebar_logo_and_title(
    logo_path="assets/SIG_Logo_RGB_Black.png",
    active_page="Job Profile Description",
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
# CSS GLOBAL SIG (VISUAL CORPORATIVO)
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
        margin-top: 10px;
    }

    /* Container minimalista */
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

    /* Texto HTML */
    .job-text {
        font-size: 16px;
        line-height: 1.45;
    }

</style>
""", unsafe_allow_html=True)

# =============================================================================
# TÍTULO DA PÁGINA COM ÍCONE
# =============================================================================
icon_path = Path("assets/icons/business review clipboard.png")

st.markdown(
    f"""
    <div class="sig-title">
        <img src="{icon_path.as_posix()}" width="22px">
        Job Profile Description
    </div>
    """,
    unsafe_allow_html=True
)

# =============================================================================
# CARREGAMENTO DO ARQUIVO DE DESCRIÇÕES
# =============================================================================
data_path = Path("data/Job Profile.xlsx")
df = load_excel_data(data_path)

if df is None or df.empty:
    st.error("Erro ao carregar Job Profile.xlsx. Verifique o arquivo.")
    st.stop()

# Normalização de colunas
df.columns = [re.sub(r'\s+', '_', col.strip().lower()) for col in df.columns]

# =============================================================================
# INTERFACE
# =============================================================================
st.markdown("""
<div class="sig-container">
<h3>Consultar Descrição de Cargo</h3>
Selecione o cargo abaixo para visualizar a descrição completa e estruturada.
</div>
""", unsafe_allow_html=True)

# Campo de busca
all_jobs = df["job_title"].dropna().unique().tolist()
job_selected = st.selectbox("Selecione o Cargo", all_jobs)

if not job_selected:
    st.stop()

# =============================================================================
# OBTÉM LINHA DO CARGO
# =============================================================================
row = df[df["job_title"] == job_selected].iloc[0]

# =============================================================================
# MONTA O BLOCO DE TEXTO
# =============================================================================
def format_section(title, content):
    """Cria um bloco com título azul SIG e texto corporativo."""
    return f"""
    <div class="sig-title">
        <img src="{icon_path.as_posix()}" width="22px">
        {title}
    </div>
    <div class="sig-container job-text">
        {content if content else "<i>Não informado</i>"}
    </div>
    """

# Campos usados pelo seu layout
sections = {
    "Resumo da Posição": row.get("summary", ""),
    "Responsabilidades Principais": row.get("key_responsibilities", ""),
    "Conhecimentos e Habilidades": row.get("knowledge_skills", ""),
    "Requisitos de Escolaridade": row.get("education", ""),
    "Experiência Necessária": row.get("experience", ""),
    "Certificações": row.get("certifications", ""),
}

# =============================================================================
# RENDERIZA SEÇÕES
# =============================================================================
for title, content in sections.items():
    st.markdown(format_section(title, content), unsafe_allow_html=True)
