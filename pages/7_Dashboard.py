# -*- coding: utf-8 -*-
# pages/7_Dashboard.py

import streamlit as st
import pandas as pd
from pathlib import Path
from utils.ui import sidebar_logo_and_title

# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Logo SIG no topo da sidebar
sidebar_logo_and_title("assets/SIG_Logo_RGB_Black.png")

# ==========================================================
# TÍTULO SIG
# ==========================================================

st.markdown("""
<div class="sig-title">
    <img src="assets/icons/data 2 performance.png">
    <span>Dashboard</span>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# SEÇÃO 1 – VISÃO GERAL
# ==========================================================

st.markdown("""
<div class="sig-card">
    <h3>Visão Consolidada da Arquitetura de Cargos</h3>
    <p>
        Este painel resume informações essenciais relacionadas à Arquitetura de Cargos 
        da SIG, incluindo dados de Job Families, Job Profiles, Níveis Organizacionais 
        (Structure Level) e lógica de Job Match (GGS).
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# SEÇÃO 2 – INDICADORES SIMPLES
# ==========================================================

# Carregamento dos arquivos Excel
jf_path = Path("data/Job Family.xlsx")
jp_path = Path("data/Job Profile.xlsx")
ls_path = Path("data/Level Structure.xlsx")

try:
    jf_df = pd.read_excel(jf_path)
    jp_df = pd.read_excel(jp_path)
    ls_df = pd.read_excel(ls_path)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="sig-card">
            <h3>Job Families</h3>
            <p style="font-size: 32px; font-weight: 700; color:#145efc;">{}</p>
        </div>
        """.format(jf_df["Job Family"].nunique()), unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="sig-card">
            <h3>Job Profiles</h3>
            <p style="font-size: 32px; font-weight: 700; color:#145efc;">{}</p>
        </div>
        """.format(jp_df["Job Title"].nunique()), unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="sig-card">
            <h3>Níveis Estruturais</h3>
            <p style="font-size: 32px; font-weight: 700; color:#145efc;">{}</p>
        </div>
        """.format(ls_df["Level"].nunique()), unsafe_allow_html=True)

except Exception as e:
    st.warning("Não foi possível carregar todos os arquivos necessários para os indicadores.")

# ==========================================================
# SEÇÃO 3 – TABELAS RESUMO
# ==========================================================

st.markdown("""
<div class="sig-card">
    <h3>Resumo das Job Families</h3>
</div>
""", unsafe_allow_html=True)

if 'jf_df' in locals():
    st.dataframe(jf_df, use_container_width=True)

st.markdown("""
<div class="sig-card">
    <h3>Resumo dos Job Profiles</h3>
</div>
""", unsafe_allow_html=True)

if 'jp_df' in locals():
    st.dataframe(jp_df, use_container_width=True)

st.markdown("""
<div class="sig-card">
    <h3>Resumo da Estrutura de Níveis</h3>
</div>
""", unsafe_allow_html=True)

if 'ls_df' in locals():
    st.dataframe(ls_df, use_container_width=True)

# ==========================================================
# RODAPÉ
# ==========================================================

st.markdown("""
<div class="sig-card">
    <p style="font-size:14px; color:#666;">
        Dashboard consolidado. Continue navegando pelo menu lateral para visualizar
        Job Families, Job Profiles, Maps, Job Match e Structure Level.
    </p>
</div>
""", unsafe_allow_html=True)
