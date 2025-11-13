# -*- coding: utf-8 -*-
# pages/1_Job_Architecture.py

import streamlit as st
from utils.ui import sidebar_logo_and_title
from utils.data_loader import load_excel_data
from pathlib import Path

# ==========================================================
# CONFIGURAÇÃO GERAL DA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="Job Architecture",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Logo no topo da sidebar
sidebar_logo_and_title("assets/SIG_Logo_RGB_Black.png")

# ==========================================================
# TÍTULO CORPORATIVO SIG
# ==========================================================

st.markdown("""
<div class="sig-title">
    <img src="assets/icons/governance.png">
    <span>Job Architecture</span>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# CONTEÚDO PRINCIPAL
# ==========================================================

st.markdown("""
<div class="sig-card">
    <h3>Visão Geral</h3>
    <p>
        A estrutura de Job Architecture é a base para garantir alinhamento global,
        consistência organizacional e clareza de carreira. Aqui você encontra:
    </p>

    <ul>
        <li>Governança e pilares estruturantes</li>
        <li>Career Bands e Global Grades</li>
        <li>Framework organizacional WTW (GGS)</li>
        <li>Integração com Job Families, Job Profiles e Job Maps</li>
    </ul>
</div>
""", unsafe_allow_html=True)


# ==========================================================
# SEGUNDO BLOCO / COMPONENTES ADICIONAIS (OPCIONAL)
# ==========================================================

st.markdown("""
<div class="sig-card">
    <h3>Objetivo da Arquitetura de Cargos</h3>
    <p>
       A arquitetura de cargos proporciona uma linguagem comum que orienta:
    </p>

    <ul>
        <li>Definição e avaliação de cargos</li>
        <li>Mobilidade interna e trilhas de carreira</li>
        <li>Estruturação salarial e políticas de remuneração</li>
        <li>Governança global e alinhamento com práticas de mercado</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# RODAPÉ / INFO EXTRA
# ==========================================================

st.markdown("""
<div class="sig-card">
    <p style="font-size:14px; color:#666;">
        Utilize o menu lateral para navegar pelas demais seções
        como Families, Job Profiles, Maps, Match (GGS) e Structure Level.
    </p>
</div>
""", unsafe_allow_html=True)
